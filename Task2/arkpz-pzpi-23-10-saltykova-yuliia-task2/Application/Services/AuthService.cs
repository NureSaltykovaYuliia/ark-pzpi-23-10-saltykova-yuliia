using Application.Abstractions.Interfaces;
using Application.DTOs;
using BCrypt.Net;
using Entities.Models;
using Infrastructure; 
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Configuration;
using Microsoft.IdentityModel.Tokens;
using System;
using System.IdentityModel.Tokens.Jwt;
using System.Security.Claims;
using System.Text;

namespace Application.Services
{
    public class AuthService : IAuthService
    {
        private readonly MyDbContext _context;
        private readonly IConfiguration _configuration;

        public AuthService(MyDbContext context, IConfiguration configuration)
        {
            _context = context;
            _configuration = configuration;
        }

        public async Task<User> Register(UserForRegistrationDto userForRegistration)
        {
            
            if (await _context.Users.AnyAsync(u => u.Email == userForRegistration.Email))
            {
                throw new Exception("Користувач з таким email вже існує.");
            }
            
           string passwordHash = BCrypt.Net.BCrypt.HashPassword(userForRegistration.Password);

           
            var user = new User
            {
                Username = userForRegistration.Username,
                Email = userForRegistration.Email,
                PasswordHash = passwordHash,
                Role = UserRole.DogOwner, 
                Bio = "" 
            };

            // Зберігаємо в БД
            _context.Users.Add(user);//Використовувати репозиторій
            await _context.SaveChangesAsync();

            return user;
        }

        public async Task<string> Login(UserForLoginDto userForLogin)
        {
           
            var user = await _context.Users.FirstOrDefaultAsync(u => u.Email == userForLogin.Email);//Використовувати репозиторій

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