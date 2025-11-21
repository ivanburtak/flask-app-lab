from flask import render_template, flash, url_for, redirect, session, request

from . import posts_bp
from .forms import PostForm
from .models import Post
from app import db


@posts_bp.route("/create", methods=["GET", "POST"])
def create_post():
    form = PostForm()

    if form.validate_on_submit():
        author_name = session.get("username", "Anonymous")

        post = Post(
            title=form.title.data,
            content=form.content.data,
            category=form.category.data,
            is_active=form.is_active.data,
            posted=form.publish_date.data,
            author=author_name
        )
        db.session.add(post)
        db.session.commit()

        flash(f"Post {form.title.data} has been added", "success")
        return redirect(url_for('.all_posts'))

    # Передаємо форму у шаблон, щоб render_field працював
    return render_template("add_post.html", form=form)

@posts_bp.route("/<int:id>/edit", methods=["GET", "POST"])
def edit_post(id):
    post = db.get_or_404(Post, id)

    form = PostForm(obj=post)
    form.publish_date.data = post.posted

    if form.validate_on_submit():
        form.populate_obj(post)
        post.posted = form.publish_date.data
        db.session.commit()
        flash("Post has been updated", "success")
        return redirect(url_for('.detail_post', post_id=id))

    return render_template("add_post.html", form=form, title="Edit Post")

@posts_bp.route("/delete/<int:id>", methods=["GET", "POST"])
def delete_post(id):
    post = db.get_or_404(Post, id)

    if request.method == "POST":
        db.session.delete(post)
        db.session.commit()
        flash("Post has been deleted", "success")
        return redirect(url_for('.all_posts'))

    return render_template("delete_confirm.html", post=post)

@posts_bp.route("/")
def all_posts():
    stmt = db.select(Post).order_by(Post.posted.desc())
    posts = db.session.scalars(stmt).all()
    return render_template("posts.html", posts=posts)

@posts_bp.route("/<int:post_id>")
def detail_post(post_id):
    post = db.get_or_404(Post, post_id)
    return render_template("detail_post.html", post=post)