app.get('/profile/:userId', async (req, res) => {
    try {
        if (!req.user) {
            return res.status(401).json({ error: 'Authentication required' });
        }

        const requestedUserId = req.params.userId;
        const isOwner = String(req.user.id) === String(requestedUserId);
        const isAdmin = req.user.role === 'admin';

        if (!isOwner && !isAdmin) {
            return res.status(403).json({ error: 'Forbidden' });
        }

        const user = await User.findById(requestedUserId).select('id name email');
        if (!user) {
            return res.status(404).json({ error: 'User not found' });
        }

        res.json(user);
    } catch (err) {
        res.status(500).json({ error: 'Internal server error' });
    }
});