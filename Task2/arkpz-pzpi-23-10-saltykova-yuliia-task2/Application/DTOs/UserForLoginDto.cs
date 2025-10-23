using System.ComponentModel.DataAnnotations;

namespace Application.DTOs
{
    public class UserForLoginDto
    {
        [Required(ErrorMessage = "Email обов'язковий")]
        [EmailAddress(ErrorMessage = "Невірний формат email")]
        public string Email { get; set; }

        [Required(ErrorMessage = "Пароль обов'язковий")]
        public string Password { get; set; }
    }
}
