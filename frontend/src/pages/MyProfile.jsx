import { useState } from 'react'
import { useAuth0 } from '@auth0/auth0-react'
import Avatar from '../components/Avatar.jsx'
import PostCard from '../components/PostCard.jsx'
import sampleImage from '../assets/hero.png'
import './MyProfile.css'

const images = [
    { id: 'demo-image', name: 'Ogledna slika', url: sampleImage },
]

function readData(storageKey, user) {
    const initialData = {
        profile: {
            display_name: user.name || '',
            username: user.nickname || '',
            avatar_url: user.picture || '',
            bio: '',
        },
        posts: [],
    }

    try {
        return JSON.parse(localStorage.getItem(storageKey)) ?? initialData
    } catch {
        return initialData
    }
}

function ProfileForm({ profile, onSave, onCancel }) {
    function handleSubmit(event) {
        event.preventDefault()
        const fields = new FormData(event.currentTarget)

        onSave({
            username: fields.get('username').trim(),
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
                    defaultValue={profile.username}
                    pattern="[A-Za-z0-9_.]+"
                    maxLength={50}
                    required
                />
            </label>

            <label>
                Ime za prikaz
                <input
                    name="display_name"
                    defaultValue={profile.display_name}
                    maxLength={255}
                    required
                />
            </label>

            <label>
                Opis
                <textarea name="bio" defaultValue={profile.bio} rows={3} />
            </label>

            <label>
                URL slike
                <input
                    name="avatar_url"
                    type="url"
                    defaultValue={profile.avatar_url}
                    maxLength={500}
                />
            </label>

            <div className="my-profile__actions">
                <button className="btn btn--primary" type="submit">
                    Spremi profil
                </button>
                <button className="btn btn--secondary" type="button" onClick={onCancel}>
                    Odustani
                </button>
            </div>
        </form>
    )
}

function PostForm({ post, onSave, onCancel }) {
    const [imageId, setImageId] = useState(post?.image_id ?? '')
    const image = images.find((entry) => entry.id === imageId)

    function handleSubmit(event) {
        event.preventDefault()
        if (!image) return

        const fields = new FormData(event.currentTarget)

        onSave({
            id: post?.id ?? crypto.randomUUID(),
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
                    <option value="">Odaberi sliku</option>
                    {images.map((entry) => (
                        <option key={entry.id} value={entry.id}>
                            {entry.name}
                        </option>
                    ))}
                </select>
            </label>

            {image && (
                <img className="my-profile__preview" src={image.url} alt={image.name} />
            )}

            <label>
                Opis
                <textarea
                    name="description"
                    defaultValue={post?.description ?? ''}
                    rows={3}
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
                <button className="btn btn--primary" type="submit" disabled={!image}>
                    Spremi post
                </button>
                <button className="btn btn--secondary" type="button" onClick={onCancel}>
                    Odustani
                </button>
            </div>
        </form>
    )
}

function ProfilePage({ user }) {
    const storageKey = `imagic:my-profile:${user.sub}`
    const [data, setData] = useState(() => readData(storageKey, user))
    const [editingProfile, setEditingProfile] = useState(false)
    const [postEditor, setPostEditor] = useState(null)
    const [pendingDelete, setPendingDelete] = useState(null)
    const [error, setError] = useState('')
    const { profile, posts } = data

    function save(nextData) {
        try {
            localStorage.setItem(storageKey, JSON.stringify(nextData))
        } catch {
            setError('Spremanje nije uspjelo. Pokušaj ponovno.')
            return false
        }

        setData(nextData)
        setError('')
        return true
    }

    function saveProfile(nextProfile) {
        if (save({ ...data, profile: nextProfile })) {
            setEditingProfile(false)
        }
    }

    function savePost(post) {
        const nextPosts = postEditor.post
            ? posts.map((entry) => entry.id === post.id ? post : entry)
            : [post, ...posts]

        if (save({ ...data, posts: nextPosts })) {
            setPostEditor(null)
        }
    }

    function removePost(id) {
        if (save({ ...data, posts: posts.filter((post) => post.id !== id) })) {
            setPendingDelete(null)

            if (postEditor?.post?.id === id) {
                setPostEditor(null)
            }
        }
    }

    return (
        <div className="my-profile">
            <h1>Moj profil</h1>
            {error && <p role="alert">{error}</p>}

            <section className="my-profile__summary" aria-label="Podaci profila">
                <Avatar
                    key={profile.avatar_url}
                    user={{ name: profile.display_name, picture: profile.avatar_url }}
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
                        onSave={savePost}
                        onCancel={() => setPostEditor(null)}
                    />
                )}

                {posts.length === 0 && <p>Još nemaš postova.</p>}

                <div className="my-profile__grid">
                    {posts.map((post) => {
                        const image = images.find((entry) => entry.id === post.image_id)

                        return (
                            <PostCard
                                key={post.id}
                                post={{ ...post, image_url: image?.url, image_name: image?.name }}
                                author={profile}
                                actions={pendingDelete === post.id ? (
                                    <>
                                        <p role="status">Želiš obrisati ovaj post?</p>
                                        <button
                                            className="btn btn--primary btn--sm"
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
                        )
                    })}
                </div>
            </section>
        </div>
    )
}

export default function MyProfile() {
    const { user } = useAuth0()

    if (!user?.sub) return <p>Profil trenutno nije dostupan.</p>

    return <ProfilePage key={user.sub} user={user} />
}