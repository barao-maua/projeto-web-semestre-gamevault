function getCsrfToken() {
    const match = document.cookie.match(/(?:^|; )csrftoken=([^;]+)/);
    return match ? decodeURIComponent(match[1]) : '';
}

async function fetchJson(url, options = {}) {
    const headers = new Headers(options.headers || {});
    if (!headers.has('X-CSRFToken')) {
        headers.set('X-CSRFToken', getCsrfToken());
    }
    if (!headers.has('X-Requested-With')) {
        headers.set('X-Requested-With', 'XMLHttpRequest');
    }

    const response = await fetch(url, {
        credentials: 'same-origin',
        ...options,
        headers,
    });

    const contentType = response.headers.get('content-type') || '';
    const text = await response.text();
    const looksLikeLoginHtml =
        text.includes('<form')
        && text.includes('csrfmiddlewaretoken')
        && (text.includes('name="username"') || text.includes('Usuario ou email'));

    if (response.redirected || looksLikeLoginHtml) {
        throw new Error('Sua sessão expirou. Faça login novamente para continuar.');
    }

    if (!contentType.includes('application/json')) {
        throw new Error('O servidor retornou uma resposta inesperada. Recarregue a página e tente novamente.');
    }

    const data = JSON.parse(text);
    if (!response.ok) {
        throw new Error(data.message || 'Nao foi possivel concluir a operacao.');
    }

    return data;
}

window.GameVaultHTTP = {
    fetchJson,
    getCsrfToken,
};
