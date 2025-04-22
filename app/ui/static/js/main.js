// Robust JS for chat UI: edit/copy icons, AJAX, and persistence

document.addEventListener("DOMContentLoaded", function() {
    // Edit icon handler
    window.startInlineEdit = function(btn, index) {
        const chatPairs = document.querySelectorAll('.chat-pair');
        if (!chatPairs[index]) return;
        const userBubble = chatPairs[index].querySelector('.bubble-content');
        const oldText = userBubble.textContent;
        const input = document.createElement('input');
        input.type = 'text';
        input.value = oldText;
        input.className = 'inline-edit-input';
        userBubble.replaceWith(input);
        input.focus();
        input.addEventListener('keydown', function(e) {
            if (e.key === 'Enter') {
                submitInlineEdit(index, input.value);
            } else if (e.key === 'Escape') {
                input.replaceWith(userBubble);
            }
        });
        input.addEventListener('blur', function() {
            input.replaceWith(userBubble);
        });
    };

    window.submitInlineEdit = function(index, value) {
    const chatPairs = document.querySelectorAll('.chat-pair');
    const pair = chatPairs[index];
    const userBubble = pair.querySelector('.bubble-content');
    // Show spinner in assistant bubble
    const assistantBubble = pair.querySelector('.assistant-bubble .bubble-content');
    const spinner = document.createElement('span');
    spinner.className = 'assistant-spinner';
    spinner.innerHTML = '<span class="loader"></span> Thinking...';
    if (assistantBubble) {
        assistantBubble.innerHTML = '';
        assistantBubble.parentNode.appendChild(spinner);
    }
    fetch(window.location.pathname + window.location.search, {
        method: 'POST',
        headers: {'Content-Type': 'application/x-www-form-urlencoded'},
        body: `inline_edit=1&edit_index=${index}&user_input=${encodeURIComponent(value)}`
    }).then(r => r.json()).then(data => {
        // Update user bubble
        userBubble.textContent = value;
        // Update assistant bubble
        if (assistantBubble) assistantBubble.innerHTML = data.answer || '[No response]';
        // Remove spinner
        if (spinner && spinner.parentNode) spinner.parentNode.removeChild(spinner);
        // Remove all chat-pairs below this index (branching)
        let next = pair.nextElementSibling;
        while (next && next.classList.contains('chat-pair')) {
            let toRemove = next;
            next = next.nextElementSibling;
            toRemove.remove();
        }
    });
};

    window.copyResponse = function(btn) {
        const bubble = btn.closest('.assistant-bubble');
        if (!bubble) return;
        const text = bubble.querySelector('.bubble-content').textContent;
        navigator.clipboard.writeText(text);
        btn.textContent = '✅';
        setTimeout(() => { btn.textContent = '📋'; }, 1200);
    };

    // New chat button handler
    const newChatBtn = document.querySelector('button[onclick*="new=1"]');
    if (newChatBtn) {
        newChatBtn.addEventListener('click', function(e) {
            e.preventDefault();
            window.location.href = '/?new=1';
        });
    }
});
