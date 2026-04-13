app.get('/user', async (req, res) => {
    try {
        const username = req.query.username;

        if (typeof username !== 'string' || !/^[a-zA-Z0-9_]{3,30}$/.test(username)) {
            return res.status(400).json({ error: 'Invalid username' });
        }

        const user = await db.collection('users').findOne(
            { username: username },
            { projection: { password: 0 } }
        );

        if (!user) {
            return res.status(404).json({ error: 'User not found' });
        }

        res.json(user);
    } catch (err) {
        res.status(500).json({ error: 'Internal server error' });
    }
});