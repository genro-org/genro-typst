// Copyright 2026 Softwell S.r.l. - SPDX-License-Identifier: Apache-2.0
let token;

export async function pythonSource(code, assets) {
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), 20000);
    try {
        if (!token) {
            const response = await fetch('/api/python/session', { signal: controller.signal });
            if (!response.ok || !response.headers.get('content-type')?.includes('application/json')) {
                throw new Error('Python needs the local playground server. Start it with npm run demo --prefix js.');
            }
            token = (await response.json()).token;
        }
        const response = await fetch('/api/python/render', {
            method: 'POST', headers: { 'Content-Type': 'application/json', 'X-Playground-Token': token },
            body: JSON.stringify({ code, assets }), signal: controller.signal,
        });
        if (response.status === 403) token = undefined;
        const result = await response.json();
        if (!response.ok || result.error) throw new Error(result.error || 'Python execution failed.');
        return result.source;
    } catch (error) {
        if (error.name === 'AbortError') throw new Error('Python request timed out. Check the local server and run again.');
        throw error;
    } finally { clearTimeout(timer); }
}
