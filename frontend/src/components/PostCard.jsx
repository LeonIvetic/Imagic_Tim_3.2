import './PostCard.css'

export default function PostCard({ post, author, actions }) {
    return (
        <article className="post-card">
            {post.image_url && (
                <img
                    className="post-card__image"
                    src={post.image_url}
                    alt={post.image_name || 'Slika objave'}
                />
            )}

            <div className="post-card__body">
                {author?.display_name && <strong>{author.display_name}</strong>}
                {post.description && <p>{post.description}</p>}

                <span className="post-card__visibility">
                    {post.is_public ? 'Javno' : 'Privatno'}
                </span>

                {actions && <div className="post-card__actions">{actions}</div>}
            </div>
        </article>
    )
}