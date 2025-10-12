using Application.DTOs;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Entities.Models;
namespace Application.Abstractions.Interfaces
{
    public interface IAuthService
    {
        Task<User> Register(UserForRegistrationDto userForRegistration);
        Task<string> Login(UserForLoginDto userForLogin);
    }
}
