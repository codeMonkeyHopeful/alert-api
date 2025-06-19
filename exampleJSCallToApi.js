async function fetchWithAuthRetry(url, options, tokens) {
  let res = await fetch(url, {
    ...options,
    headers: {
      Authorization: `Bearer ${tokens.access_token}`,
      ...options.headers,
    },
  });

  if (res.status === 401) {
    // Token might be expired — try refresh
    const refreshRes = await fetch("/auth/refresh", {
      method: "POST",
      headers: { Authorization: `Bearer ${tokens.refresh_token}` },
    });

    if (refreshRes.ok) {
      const { access_token } = await refreshRes.json();
      tokens.access_token = access_token; // update stored token

      // Retry original request
      res = await fetch(url, {
        ...options,
        headers: {
          Authorization: `Bearer ${tokens.access_token}`,
          ...options.headers,
        },
      });
    }
  }

  return res;
}
