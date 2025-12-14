using Application.Abstractions.Interfaces;
using Application.DTOs;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using System.Security.Claims;

namespace MyDogSpace.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
   
    public class SmartDevicesController : ControllerBase
    {
        private readonly ISmartDeviceService _deviceService;

        public SmartDevicesController(ISmartDeviceService deviceService)
        {
            _deviceService = deviceService;
        }

        private int GetCurrentUserId() => int.Parse(User.FindFirstValue(ClaimTypes.NameIdentifier));

        private string GetCurrentUserRole() => User.FindFirstValue(ClaimTypes.Role) ?? "DogOwner";

        [HttpGet]
        public async Task<IActionResult> GetAllDevices()
        {
            var devices = await _deviceService.GetAllDevicesAsync(GetCurrentUserId(), GetCurrentUserRole());
            return Ok(devices);
        }

        [HttpGet("{id}")]
        public async Task<IActionResult> GetDeviceById(int id)
        {
            try
            {
                var device = await _deviceService.GetDeviceByIdAsync(id, GetCurrentUserId());
                if (device == null) return NotFound();
                return Ok(device);
            }
            catch (UnauthorizedAccessException)
            {
                return Forbid();
            }
            catch (Exception ex)
            {
                return BadRequest(new { message = ex.Message });
            }
        }

        [HttpGet("dog/{dogId}")]
        public async Task<IActionResult> GetDeviceByDogId(int dogId)
        {
            try
            {
                var device = await _deviceService.GetDeviceByDogIdAsync(dogId, GetCurrentUserId());
                if (device == null) return NotFound("Пристрій не знайдено");
                return Ok(device);
            }
            catch (UnauthorizedAccessException)
            {
                return Forbid();
            }
            catch (Exception ex)
            {
                return BadRequest(new { message = ex.Message });
            }
        }

        [HttpPost]
        public async Task<IActionResult> CreateDevice([FromBody] CreateSmartDeviceDto deviceDto)
        {
            if (!ModelState.IsValid)
                return BadRequest(ModelState);

            try
            {
                var createdDevice = await _deviceService.CreateDeviceAsync(deviceDto, GetCurrentUserId());
                return CreatedAtAction(nameof(GetDeviceById), new { id = createdDevice.Id }, createdDevice);
            }
            catch (UnauthorizedAccessException)
            {
                return Forbid();
            }
            catch (Exception ex)
            {
                return BadRequest(new { message = ex.Message });
            }
        }

        [HttpPut("{id}")]
        public async Task<IActionResult> UpdateDevice(int id, [FromBody] UpdateSmartDeviceDto deviceDto)
        {
            if (!ModelState.IsValid)
                return BadRequest(ModelState);

            try
            {
                await _deviceService.UpdateDeviceAsync(id, deviceDto, GetCurrentUserId());
                return NoContent();
            }
            catch (UnauthorizedAccessException)
            {
                return Forbid();
            }
            catch (Exception ex)
            {
                return BadRequest(new { message = ex.Message });
            }
        }

        [HttpDelete("{id}")]
        public async Task<IActionResult> DeleteDevice(int id)
        {
            try
            {
                await _deviceService.DeleteDeviceAsync(id, GetCurrentUserId());
                return NoContent();
            }
            catch (UnauthorizedAccessException)
            {
                return Forbid();
            }
            catch (Exception ex)
            {
                return BadRequest(new { message = ex.Message });
            }
        }

        // Endpoints для роботи пристрою (без авторизації)
        [AllowAnonymous]
        [HttpPost("register-device")]
        public async Task<IActionResult> RegisterDevice([FromBody] RegisterDeviceDto registerDto)
        {
            if (!ModelState.IsValid)
                return BadRequest(ModelState);

            try
            {
                var device = await _deviceService.RegisterDeviceAsync(registerDto.DeviceGuid);
                return Ok(device);
            }
            catch (Exception ex)
            {
                return BadRequest(new { message = ex.Message });
            }
        }

        [AllowAnonymous]
        [HttpGet("device/{deviceGuid}/dog")]
        public async Task<IActionResult> GetDogIdByDeviceGuid(string deviceGuid)
        {
            try
            {
                var dogId = await _deviceService.GetDogIdByDeviceGuidAsync(deviceGuid);
                if (dogId == null)
                    return Ok(new { dogId = (int?)null, message = "Собака ще не призначена цьому пристрою" });

                return Ok(new { dogId = dogId.Value });
            }
            catch (Exception ex)
            {
                return BadRequest(new { message = ex.Message });
            }
        }

        [HttpPost("device/{deviceGuid}/assign")]
        public async Task<IActionResult> AssignDeviceToDog(string deviceGuid, [FromBody] AssignDeviceDto request)
        {
            try
            {
                // Передаем deviceGuid из URL и dogId из тіла запиту
                await _deviceService.AssignDeviceToDogAsync(deviceGuid, request.DogId, GetCurrentUserId());

                return Ok(new { message = "Пристрій успішно прив'язано до вибраної собаки" });
            }
            catch (Exception ex)
            {
                return BadRequest(new { message = ex.Message });
            }
        }

        // Endpoint для відправки телеметрії БЕЗ авторизації (для IoT пристроїв)
        [AllowAnonymous]
        [HttpPut("device/{id}/telemetry")]
        public async Task<IActionResult> UpdateDeviceTelemetry(int id, [FromBody] UpdateSmartDeviceDto deviceDto)
        {
            if (!ModelState.IsValid)
                return BadRequest(ModelState);

            try
            {
                await _deviceService.UpdateDeviceTelemetryAsync(id, deviceDto);
                return NoContent();
            }
            catch (Exception ex)
            {
                return BadRequest(new { message = ex.Message });
            }
        }
    }
}
