export default {
    darkMode: ['class'],
    content: ['./index.html', './src/**/*.{ts,tsx}'],
    theme: {
        extend: {
            colors: {
                bg: 'hsl(var(--bg))',
                fg: 'hsl(var(--fg))',
                card: 'hsl(var(--card))',
                muted: 'hsl(var(--muted))',
                border: 'hsl(var(--border))',
                brand: {
                    50: '#f0f9ff',
                    100: '#e0f2fe',
                    200: '#bae6fd',
                    300: '#7dd3fc',
                    400: '#38bdf8',
                    500: '#0ea5e9',
                    600: '#0284c7',
                    700: '#0369a1',
                    800: '#075985',
                    900: '#0c4a6e',
                },
            },
            boxShadow: {
                glass: '0 20px 80px rgba(2, 132, 199, 0.15)',
            },
            backgroundImage: {
                'grid-fade': 'radial-gradient(circle at top left, rgba(14,165,233,0.18), transparent 42%), radial-gradient(circle at 80% 20%, rgba(56,189,248,0.16), transparent 30%), linear-gradient(180deg, rgba(2,6,23,0.96), rgba(15,23,42,0.96))',
            },
        },
    },
    plugins: [],
};
