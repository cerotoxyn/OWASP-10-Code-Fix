import at.favre.lib.crypto.bcrypt.BCrypt;

public boolean login(String inputPassword, User user) {
    BCrypt.Result result = BCrypt.verifyer()
        .verify(inputPassword.toCharArray(), user.getPasswordHash());
    return result.verified;
}