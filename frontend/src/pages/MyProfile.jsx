import { useEffect, useState } from 'react'
import Avatar from '../components/Avatar.jsx'
import PostCard from '../components/PostCard.jsx'
import { useData } from '../data/useData.js'
import { useImageUrl, usePostImageUrl } from '../data/images.js'
import './MyProfile.css'

// Moja javna stranica (UC-004): profil i postovi. Podaci dolaze s backenda
// (/api/users/me, /api/posts), pa ih vide i drugi korisnici te ostaju nakon odjave.

function ProfileForm({ profile, busy, onSave, onCancel }) {
    function handleSubmit(event) {
        event.preventDefault()
        const fields = new FormData(event.currentTarget)

        // Korisničko ime nije obavezno dok ga korisnik ne odabere; prazno se ne šalje,
        // pa se ostali podaci profila mogu spremiti i bez njega.
        const username = fields.get('username').trim()
        onSave({
            ...(username && { username }),
            display_name: fields.get('display_name').trim(),
            bio: fields.get('bio').trim(),
            avatar_url: fields.get('avatar_url').trim(),
        })
    }

    return (
        <form className="my-profile__form" onSubmit={handleSubmit}>
            <h2>Uredi profil</h2>

            <label>
                Korisničko ime
                <input
                    name="username"
                    defaultValue={profile.username ?? ''}
                    pattern="[A-Za-z0-9_.]+"
                    maxLength={50}
                    // Jednom odabrano korisničko ime ne može se obrisati (backend), samo promijeniti.
                    required={Boolean(profile.username)}
                />
            </label>

            <label>
                Ime za prikaz
                <input
                    name="display_name"
                    defaultValue={profile.display_name ?? ''}
                    maxLength={255}
                />
            </label>

            <label>
                Opis
                <textarea name="bio" defaultValue={profile.bio ?? ''} rows={3} maxLength={1000} />
            </label>

            <label>
                URL slike
                <input
                    name="avatar_url"
                    type="url"
                    defaultValue={profile.avatar_url ?? ''}
                    maxLength={500}
                />
            </label>

            <div className="my-profile__actions">
                <button className="btn btn--primary" type="submit" disabled={busy}>
                    {busy ? 'Spremanje…' : 'Spremi profil'}
                </button>
                <button className="btn btn--secondary" type="button" onClick={onCancel}>
                    Odustani
                </button>
            </div>
        </form>
    )
}

function PostForm({ post, images, busy, onSave, onCancel }) {
    const [imageId, setImageId] = useState(post ? String(post.image_id) : '')
    const image = images.find((entry) => String(entry.id) === imageId)
    const preview = useImageUrl(image?.id, image?.updated_at)

    function handleSubmit(event) {
        event.preventDefault()
        if (!image) return

        const fields = new FormData(event.currentTarget)

        onSave({
            image_id: image.id,
            description: fields.get('description').trim(),
            is_public: fields.has('is_public'),
        })
    }

    return (
        <form className="my-profile__form" onSubmit={handleSubmit}>
            <h3>{post ? 'Uredi post' : 'Novi post'}</h3>

            <label>
                Slika iz radne okoline
                <select
                    value={imageId}
                    onChange={(event) => setImageId(event.target.value)}
                    required
                >
                    <option value="">
                        {images.length ? 'Odaberi sliku' : 'Radna okolina nema slika'}
                    </option>
                    {images.map((entry) => (
                        <option key={entry.id} value={entry.id}>
                            {entry.name}
                        </option>
                    ))}
                </select>
            </label>

            {preview.url && (
                <img className="my-profile__preview" src={preview.url} alt={image.name} />
            )}

            <label>
                Opis
                <textarea
                    name="description"
                    defaultValue={post?.description ?? ''}
                    rows={3}
                    maxLength={2000}
                />
            </label>

            <label className="my-profile__visibility">
                <input
                    name="is_public"
                    type="checkbox"
                    defaultChecked={post?.is_public ?? false}
                />
                Javno
            </label>

            <div className="my-profile__actions">
                <button className="btn btn--primary" type="submit" disabled={!image || busy}>
                    {busy ? 'Spremanje…' : 'Spremi post'}
                </button>
                <button className="btn btn--secondary" type="button" onClick={onCancel}>
                    Odustani
                </button>
            </div>
        </form>
    )
}

// PostCard prima gotov image_url; ovdje ga dohvaćamo preko /api/posts/{id}/image.
function ProfilePostCard({ post, author, actions }) {
    const { url } = usePostImageUrl(post.id, `${post.image_id}-${post.image_updated_at}`)
    return (
        <PostCard
            post={{ ...post, image_url: url }}
            author={author}
            actions={actions}
        />
    )
}

export default function MyProfile() {
    const data = useData()
    const [state, setState] = useState(null) // { profile, posts, images }
    const [loadError, setLoadError] = useState('')
    const [editingProfile, setEditingProfile] = useState(false)
    const [postEditor, setPostEditor] = useState(null)
    const [pendingDelete, setPendingDelete] = useState(null)
    const [busy, setBusy] = useState(false)
    const [error, setError] = useState('')

    // data.version se mijenja nakon svake izmjene, pa se podaci ponovno učitaju.
    useEffect(() => {
        let cancelled = false
        Promise.all([data.getMe(), data.listMyPosts(), data.listAllImages()])
            .then(([profile, posts, images]) => {
                if (!cancelled) {
                    setState({ profile, posts, images })
                    setLoadError('')
                }
            })
            .catch((err) => !cancelled && setLoadError(err.message))
        return () => {
            cancelled = true
        }
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [data.version])

    // Izvodi izmjenu na backendu; greška (npr. zauzeto korisničko ime) ostaje vidljiva.
    async function run(action) {
        setBusy(true)
        setError('')
        try {
            await action()
            return true
        } catch (err) {
            setError(err.message)
            return false
        } finally {
            setBusy(false)
        }
    }

    async function saveProfile(fields) {
        if (await run(() => data.updateMe(fields))) {
            setEditingProfile(false)
        }
    }

    async function savePost(fields) {
        const editing = postEditor.post
        const ok = await run(() =>
            editing ? data.updatePost(editing.id, fields) : data.createPost(fields),
        )
        if (ok) setPostEditor(null)
    }

    async function removePost(id) {
        if (await run(() => data.deletePost(id))) {
            setPendingDelete(null)

            if (postEditor?.post?.id === id) {
                setPostEditor(null)
            }
        }
    }

    if (loadError) return <p role="alert">{loadError}</p>
    if (!state) return <p>Učitavanje…</p>

    const { profile, posts, images } = state

    return (
        <div className="my-profile">
            <h1>Moj profil</h1>
            {error && <p role="alert">{error}</p>}

            <section className="my-profile__summary" aria-label="Podaci profila">
                <Avatar
                    key={profile.avatar_url}
                    user={{ name: profile.display_name, email: profile.email, picture: profile.avatar_url }}
                />

                <div>
                    <h2>{profile.display_name || 'Korisnik'}</h2>
                    {profile.username && <p>@{profile.username}</p>}
                    {profile.bio && <p>{profile.bio}</p>}
                </div>

                {!editingProfile && (
                    <button
                        className="btn btn--secondary"
                        onClick={() => setEditingProfile(true)}
                    >
                        Uredi profil
                    </button>
                )}
            </section>

            {editingProfile && (
                <ProfileForm
                    profile={profile}
                    busy={busy}
                    onSave={saveProfile}
                    onCancel={() => setEditingProfile(false)}
                />
            )}

            <section className="my-profile__posts" aria-labelledby="my-posts-title">
                <div className="my-profile__heading">
                    <h2 id="my-posts-title">Moji postovi</h2>
                    {!postEditor && (
                        <button
                            className="btn btn--primary"
                            onClick={() => setPostEditor({ post: null })}
                        >
                            Novi post
                        </button>
                    )}
                </div>

                {postEditor && (
                    <PostForm
                        key={postEditor.post?.id ?? 'new'}
                        post={postEditor.post}
                        images={images}
                        busy={busy}
                        onSave={savePost}
                        onCancel={() => setPostEditor(null)}
                    />
                )}

                {posts.length === 0 && <p>Još nemaš postova.</p>}

                <div className="my-profile__grid">
                    {posts.map((post) => (
                        <ProfilePostCard
                            key={post.id}
                            post={post}
                            author={profile}
                            actions={pendingDelete === post.id ? (
                                <>
                                    <p role="status">Želiš obrisati ovaj post?</p>
                                    <button
                                        className="btn btn--primary btn--sm"
                                        disabled={busy}
                                        onClick={() => removePost(post.id)}
                                    >
                                        Potvrdi brisanje
                                    </button>
                                    <button
                                        className="btn btn--secondary btn--sm"
                                        onClick={() => setPendingDelete(null)}
                                    >
                                        Odustani
                                    </button>
                                </>
                            ) : (
                                <>
                                    <button
                                        className="btn btn--secondary btn--sm"
                                        onClick={() => setPostEditor({ post })}
                                    >
                                        Uredi
                                    </button>
                                    <button
                                        className="btn btn--ghost btn--sm"
                                        onClick={() => setPendingDelete(post.id)}
                                    >
                                        Obriši
                                    </button>
                                </>
                            )}
                        />
                    ))}
                </div>
            </section>
        </div>
    )
}
