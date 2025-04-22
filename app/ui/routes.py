from flask import render_template, request, redirect, url_for, flash
import requests
import os

def init_routes(app):
    # from flask import get_flashed_messages
    API_URL = os.environ.get("API_URL", "http://localhost:8000")

    from flask import session, request, redirect, url_for
    import uuid
    from urllib.parse import urlencode

    @app.route("/delete_session")
    def delete_session():
        session_id = request.args.get('session')
        all_chats = session.get('all_chats', {})
        if session_id and session_id in all_chats:
            all_chats.pop(session_id)
            session['all_chats'] = all_chats
        # Redirect to main page (new chat if available)
        return redirect(url_for('index'))

    @app.route("/", methods=["GET", "POST"])
    def index():
        answer = None
        user_input = ''
        error = None
        # --- Multi-session logic ---
        all_chats = session.get('all_chats', {})  # {session_id: {'title': ..., 'history': [...]}}
        session_id = request.args.get('session')
        new_chat = request.args.get('new')
        if not all_chats:
            all_chats = {}
        if new_chat:
            # Start a new session
            session_id = str(uuid.uuid4())
            all_chats[session_id] = {'title': 'New Chat', 'history': []}
            session['all_chats'] = all_chats
            session.modified = True  # Ensure Flask saves the new session
            return redirect(url_for('index', session=session_id))
        if not session_id or session_id not in all_chats:
            # If no session, pick the latest or create one
            if all_chats:
                session_id = list(all_chats.keys())[-1]
            else:
                session_id = str(uuid.uuid4())
                all_chats[session_id] = {'title': 'New Chat', 'history': []}
                session['all_chats'] = all_chats
                return redirect(url_for('index', session=session_id))
        chat_obj = all_chats[session_id]
        chat_history = chat_obj['history']
        edit_index = request.args.get('edit', type=int)
        if request.method == "POST":
            if 'inline_edit' in request.form:
                # Inline edit mode (AJAX)
                edit_index = int(request.form.get('edit_index', -1))
                user_input = request.form.get('user_input', '').strip()
                if 0 <= edit_index < len(chat_history) and user_input:
                    # Build context up to the message before the edit
                    context = '\n'.join([f"Q: {q}\nA: {a}" for q, a in chat_history[:edit_index]])
                    try:
                        resp = requests.post(f"{API_URL}/chat", json={"query": user_input, "history": context})
                        if resp.ok:
                            answer = resp.json().get("answer")
                            # Replace the old query/response at edit_index
                            chat_history[edit_index] = (user_input, answer)
                            all_chats[session_id]['history'] = chat_history
                            session.modified = True
                            session['all_chats'] = all_chats
                            return {"answer": answer}
                        else:
                            return {"answer": "[Error: " + resp.text + "]"}
                    except Exception as e:
                        return {"answer": f"[Chat failed: {e}]"}
                else:
                    return {"answer": "[Invalid edit request]"}
            else:
                user_input = request.form.get("user_input")
                if user_input:
                    # For follow-up: pass chat history as context
                    context = '\n'.join([f"Q: {q}\nA: {a}" for q, a in chat_history])
                    try:
                        resp = requests.post(f"{API_URL}/chat", json={"query": user_input, "history": context})
                        if resp.ok:
                            answer = resp.json().get("answer")
                            # Append to chat history
                            chat_history.append((user_input, answer))
                            # Predict title if this is the first message
                            if len(chat_history) == 1:
                                title = user_input[:40] + ("..." if len(user_input) > 40 else "")
                                all_chats[session_id]['title'] = title
                            all_chats[session_id]['history'] = chat_history
                            session.modified = True
                            session['all_chats'] = all_chats
                            user_input = ''  # Clear input after send
                        else:
                            error = "Error: " + resp.text
                            flash(error, "danger")
                    except Exception as e:
                        error = f"Chat failed: {e}"
                        flash(error, "danger")
        # Prepare sidebar session list: [(session_id, title, active)]
        chat_sessions = [(sid, obj['title'], sid == session_id) for sid, obj in all_chats.items()]
        return render_template(
            "index.html",
            answer=answer,
            user_input=user_input,
            chat_history=chat_history,
            chat_sessions=chat_sessions,
            active_session=session_id,
            show_upload_nav=True
        )

    @app.route("/upload", methods=["GET", "POST"])
    def upload():
        if request.method == "POST":
            file = request.files.get("file")
            if file:
                try:
                    files = {"file": (file.filename, file.stream, file.mimetype)}
                    resp = requests.post(f"{API_URL}/upload", files=files)
                    if resp.ok:
                        flash("File uploaded and ingested successfully!", "success")
                    else:
                        flash("Upload failed: " + resp.text, "danger")
                except Exception as e:
                    flash(f"Upload failed: {e}", "danger")
                return redirect(url_for("upload"))
        return render_template("upload.html", show_upload_nav=True)
