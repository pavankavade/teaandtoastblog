// Cloudflare Pages Function Middleware: Protects all /studio/* routes with HTTP Basic Auth
export async function onRequest({ request, next, env }: { request: Request; next: () => Promise<Response>; env: Record<string, string> }) {
  const expectedUser = env.STUDIO_USERNAME || 'creator';
  const expectedPass = env.STUDIO_PASSWORD || 'toast2026';

  const authHeader = request.headers.get('Authorization');

  if (authHeader && authHeader.startsWith('Basic ')) {
    const base64 = authHeader.substring(6);
    try {
      const decoded = atob(base64);
      const [user, pass] = decoded.split(':');
      if (user === expectedUser && pass === expectedPass) {
        return next();
      }
    } catch (e) {
      // Fallback to 401 on decode error
    }
  }

  return new Response('401 Unauthorized: Tea & Toast Creator Studio Authentication Required', {
    status: 401,
    headers: {
      'WWW-Authenticate': 'Basic realm="Tea & Toast Creator Studio", charset="UTF-8"',
      'Content-Type': 'text/plain; charset=utf-8',
      'X-Robots-Tag': 'noindex, nofollow',
    },
  });
}
