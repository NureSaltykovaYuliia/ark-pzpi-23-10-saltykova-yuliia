using Application.Abstractions.Interfaces;
using Application.DTOs;
using Entities.Models;
using Microsoft.Extensions.Configuration;
using Microsoft.IdentityModel.Tokens;
using System.IdentityModel.Tokens.Jwt;
using System.Security.Claims;
using System.Text;

namespace Application.Services
{
    public class AuthService : IAuthService
    {

        private readonly IUserRepository _userRepository;
        private readonly IAdminCodeRepository _adminCodeRepository;
        private readonly IConfiguration _configuration;


        public AuthService(IUserRepository userRepository, IAdminCodeRepository adminCodeRepository, IConfiguration configuration)
        {
            _userRepository = userRepository;
            _adminCodeRepository = adminCodeRepository;
            _configuration = configuration;
        }

        public async Task<User> Register(UserForRegistrationDto userForRegistration)
        {

            if (await _userRepository.DoesUserExistAsync(userForRegistration.Email))
            {
                throw new Exception("Користувач з таким email вже існує.");
            }

            // Перевірка коду адміністратора
            AdminCode adminCode = null;
            UserRole userRole = UserRole.DogOwner;

            if (!string.IsNullOrWhiteSpace(userForRegistration.AdminCode))
            {
                adminCode = await _adminCodeRepository.GetByCodeAsync(userForRegistration.AdminCode);

                if (adminCode == null)
                {
                    throw new Exception("Невірний код адміністратора.");
                }

                if (adminCode.IsUsed)
                {
                    throw new Exception("Код адміністратора вже використаний.");
                }

                userRole = UserRole.Admin;
            }

            string passwordHash = BCrypt.Net.BCrypt.HashPassword(userForRegistration.Password);

            var user = new User
            {
                Username = userForRegistration.Username,
                Email = userForRegistration.Email,
                PasswordHash = passwordHash,
                Role = userRole,
                Bio = ""
            };


            var createdUser = await _userRepository.AddUserAsync(user);

            // Позначити код як використаний
            if (adminCode != null)
            {
                await _adminCodeRepository.MarkAsUsedAsync(adminCode.Id, createdUser.Id);
            }

            return createdUser;
        }

        public async Task<string> Login(UserForLoginDto userForLogin)
        {
    
            var user = await _userRepository.GetUserByEmailAsync(userForLogin.Email);

            if (user == null || !BCrypt.Net.BCrypt.Verify(userForLogin.Password, user.PasswordHash))
            {
                throw new Exception("Неправильний email або пароль.");
            }

            return CreateToken(user);
        }

        private string CreateToken(User user)
        {
            var claims = new List<Claim>
            {
                new Claim(ClaimTypes.NameIdentifier, user.Id.ToString()),
                new Claim(ClaimTypes.Name, user.Username),
                new Claim(ClaimTypes.Role, user.Role.ToString())
            };

            var key = new SymmetricSecurityKey(Encoding.UTF8.GetBytes(_configuration.GetSection("AppSettings:Token").Value));
            var creds = new SigningCredentials(key, SecurityAlgorithms.HmacSha512Signature);

            var tokenDescriptor = new SecurityTokenDescriptor
            {
                Subject = new ClaimsIdentity(claims),
                Expires = DateTime.Now.AddDays(1),
                SigningCredentials = creds
            };

            var tokenHandler = new JwtSecurityTokenHandler();
            var token = tokenHandler.CreateToken(tokenDescriptor);

            return tokenHandler.WriteToken(token);
        }
    }
}