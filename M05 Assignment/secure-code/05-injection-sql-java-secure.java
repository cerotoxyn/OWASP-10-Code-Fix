String username = request.getParameter("username");
String query = "SELECT * FROM users WHERE username = ?";

PreparedStatement stmt = connection.prepareStatement(query);
stmt.setString(1, username);

ResultSet rs = stmt.executeQuery();