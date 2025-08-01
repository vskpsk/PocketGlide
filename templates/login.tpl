<!DOCTYPE html>
<html>
    <head>
        <link rel="manifest" href="/manifest.json">
        <meta name="theme-color" content="#3b82f6">
        <link rel="icon" href="/static/icon-192.png" type="image/png" sizes="192x192">
        <link rel="shortcut icon" href="/favicon.ico" type="image/x-icon">
        <meta charset="UTF-8">
        <title>Login – PocketGlide</title>
        <script src="https://cdn.tailwindcss.com"></script>
    </head>
    <body class="bg-white text-gray-900 font-sans h-screen flex items-center justify-center">
        <form method="post" class="bg-gray-50 border border-gray-200 rounded-xl shadow-sm p-6 w-full max-w-sm space-y-4">
            <h1 class="text-xl font-semibold text-center">PocketGlide Login</h1>
            <input type="password" name="password" placeholder="Enter password"
                class="border px-3 py-2 rounded w-full text-sm" required>
            <button type="submit"
                class="bg-blue-600 text-white px-4 py-2 rounded w-full hover:bg-blue-700 text-sm">
                Login
            </button>
        </form>
    </body>
</html>