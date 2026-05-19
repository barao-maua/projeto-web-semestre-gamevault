document.addEventListener('DOMContentLoaded', function() {
    const password1 =
        document.getElementById('id_password1') ||
        document.getElementById('id_new_password1');
    const password2 =
        document.getElementById('id_password2') ||
        document.getElementById('id_new_password2');
    const passwordMatchStatus = document.getElementById('password-match-status');

    if (!password1 || !password2 || !passwordMatchStatus) {
        return;
    }

    function toggleRule(ruleName, isValid) {
        const rule = document.querySelector(`[data-password-rule="${ruleName}"]`);
        if (!rule) {
            return;
        }

        rule.classList.toggle('is-valid', isValid);
        const icon = rule.querySelector('.password-rule-icon');
        if (icon) {
            icon.textContent = isValid ? '✓' : '•';
        }
    }

    function updatePasswordFeedback() {
        const value = password1.value;
        toggleRule('length', value.length >= 8);
        toggleRule('uppercase', /[A-Z]/.test(value));
        toggleRule('lowercase', /[a-z]/.test(value));
        toggleRule('number', /\d/.test(value));
        toggleRule('special', /[^A-Za-z0-9]/.test(value));
    }

    function updatePasswordMatch() {
        const hasConfirmation = password2.value.length > 0;
        const matches = hasConfirmation && password1.value === password2.value;

        passwordMatchStatus.classList.remove('is-valid', 'is-invalid');

        if (!hasConfirmation) {
            passwordMatchStatus.textContent = 'Digite a confirmação para comparar as senhas.';
            return;
        }

        if (matches) {
            passwordMatchStatus.textContent = 'As senhas coincidem.';
            passwordMatchStatus.classList.add('is-valid');
            return;
        }

        passwordMatchStatus.textContent = 'As senhas ainda não coincidem.';
        passwordMatchStatus.classList.add('is-invalid');
    }

    password1.addEventListener('input', function() {
        updatePasswordFeedback();
        updatePasswordMatch();
    });

    password2.addEventListener('input', updatePasswordMatch);

    updatePasswordFeedback();
    updatePasswordMatch();
});
