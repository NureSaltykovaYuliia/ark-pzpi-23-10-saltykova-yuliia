using Application.Abstractions.Interfaces;
using Application.DTOs;
using Microsoft.AspNetCore.Mvc;
using Entities.Models;

namespace MyDogSpace.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class AuthController : ControllerBase
    {
        private readonly IAuthService _authService;

        public AuthController(IAuthService authService)
        {
            _authService = authService;
        }

        [HttpPost("register")]
        public async Task<IActionResult> Register(UserForRegistrationDto userForRegistrationDto)
        {
            try
            {
                User createdUser = await _authService.Register(userForRegistrationDto);
                return Ok(new { message = "Реєстрація успішна" });
            }
            catch (Exception ex)
            {
                return BadRequest(new { message = ex.Message });
            }
        }

        [HttpPost("login")]
        public async Task<IActionResult> Login(UserForLoginDto userForLoginDto)
        {
            try
            {
                string token = await _authService.Login(userForLoginDto);
                return Ok(new { token }); 
            }
            catch (Exception ex)
            {
                return Unauthorized(new { message = ex.Message });
            }
        }
    }
}