import at.favre.lib.crypto.bcrypt.BCrypt;

public String hashPassword(String password) {
    return BCrypt.withDefaults().hashToString(12, password.toCharArray());
}

public boolean verifyPassword(String password, String storedHash) {
    BCrypt.Result result = BCrypt.verifyer().verify(password.toCharArray(), storedHash);
    return result.verified;
}