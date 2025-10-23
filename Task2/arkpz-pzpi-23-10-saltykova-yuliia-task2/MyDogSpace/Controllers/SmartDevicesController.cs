using Application.Abstractions.Interfaces;
using Application.DTOs;
using Entities.Models;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using System.Security.Claims;

namespace MyDogSpace.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    [Authorize]
    public class SmartDevicesController : ControllerBase
    {
        private readonly ISmartDeviceRepository _deviceRepository;
        private readonly IDogRepository _dogRepository;

        public SmartDevicesController(ISmartDeviceRepository deviceRepository, IDogRepository dogRepository)
        {
            _deviceRepository = deviceRepository;
            _dogRepository = dogRepository;
        }

        private int GetCurrentUserId() => int.Parse(User.FindFirstValue(ClaimTypes.NameIdentifier));

        [HttpGet]
        public async Task<IActionResult> GetAllDevices()
        {
            var devices = await _deviceRepository.GetAllAsync();
            var deviceDtos = devices.Select(d => new SmartDeviceDto
            {
                Id = d.Id,
                DeviceGuid = d.DeviceGuid,
                LastLatitude = d.LastLatitude,
                LastLongitude = d.LastLongitude,
                BatteryLevel = d.BatteryLevel,
                DogId = d.DogId,
                DogName = d.Dog?.Name
            });
            return Ok(deviceDtos);
        }

        [HttpGet("{id}")]
        public async Task<IActionResult> GetDeviceById(int id)
        {
            var device = await _deviceRepository.GetByIdAsync(id);
            if (device == null) return NotFound();

            var dog = await _dogRepository.GetByIdAsync(device.DogId);
            if (dog != null && dog.OwnerId != GetCurrentUserId()) return Forbid();

            var deviceDto = new SmartDeviceDto
            {
                Id = device.Id,
                DeviceGuid = device.DeviceGuid,
                LastLatitude = device.LastLatitude,
                LastLongitude = device.LastLongitude,
                BatteryLevel = device.BatteryLevel,
                DogId = device.DogId,
                DogName = device.Dog?.Name
            };
            return Ok(deviceDto);
        }

        [HttpGet("dog/{dogId}")]
        public async Task<IActionResult> GetDeviceByDogId(int dogId)
        {
            var dog = await _dogRepository.GetByIdAsync(dogId);
            if (dog == null) return NotFound("Собака не знайдена");
            if (dog.OwnerId != GetCurrentUserId()) return Forbid();

            var device = await _deviceRepository.GetByDogIdAsync(dogId);
            if (device == null) return NotFound("Пристрій не знайдено");

            var deviceDto = new SmartDeviceDto
            {
                Id = device.Id,
                DeviceGuid = device.DeviceGuid,
                LastLatitude = device.LastLatitude,
                LastLongitude = device.LastLongitude,
                BatteryLevel = device.BatteryLevel,
                DogId = device.DogId,
                DogName = device.Dog?.Name
            };
            return Ok(deviceDto);
        }

        [HttpPost]
        public async Task<IActionResult> CreateDevice([FromBody] CreateSmartDeviceDto deviceDto)
        {
            if (!ModelState.IsValid)
                return BadRequest(ModelState);

            var dog = await _dogRepository.GetByIdAsync(deviceDto.DogId);
            if (dog == null) return NotFound("Собака не знайдена");
            if (dog.OwnerId != GetCurrentUserId()) return Forbid();

            var existingDevice = await _deviceRepository.GetByDogIdAsync(deviceDto.DogId);
            if (existingDevice != null)
                return BadRequest("До цієї собаки вже прикріплений пристрій");

            var device = new SmartDevice
            {
                DeviceGuid = deviceDto.DeviceGuid,
                DogId = deviceDto.DogId,
                LastLatitude = 0,
                LastLongitude = 0,
                BatteryLevel = 100
            };

            var createdDevice = await _deviceRepository.AddAsync(device);
            var resultDto = new SmartDeviceDto
            {
                Id = createdDevice.Id,
                DeviceGuid = createdDevice.DeviceGuid,
                LastLatitude = createdDevice.LastLatitude,
                LastLongitude = createdDevice.LastLongitude,
                BatteryLevel = createdDevice.BatteryLevel,
                DogId = createdDevice.DogId,
                DogName = dog?.Name
            };
            return CreatedAtAction(nameof(GetDeviceById), new { id = createdDevice.Id }, resultDto);
        }

        [HttpPut("{id}")]
        public async Task<IActionResult> UpdateDevice(int id, [FromBody] UpdateSmartDeviceDto deviceDto)
        {
            if (!ModelState.IsValid)
                return BadRequest(ModelState);

            var device = await _deviceRepository.GetByIdAsync(id);
            if (device == null) return NotFound();

            var dog = await _dogRepository.GetByIdAsync(device.DogId);
            if (dog != null && dog.OwnerId != GetCurrentUserId()) return Forbid();

            device.LastLatitude = deviceDto.LastLatitude;
            device.LastLongitude = deviceDto.LastLongitude;
            device.BatteryLevel = deviceDto.BatteryLevel;

            await _deviceRepository.UpdateAsync(device);
            return NoContent();
        }

        [HttpDelete("{id}")]
        public async Task<IActionResult> DeleteDevice(int id)
        {
            var device = await _deviceRepository.GetByIdAsync(id);
            if (device == null) return NotFound();

            var dog = await _dogRepository.GetByIdAsync(device.DogId);
            if (dog != null && dog.OwnerId != GetCurrentUserId()) return Forbid();

            await _deviceRepository.DeleteAsync(id);
            return NoContent();
        }
    }
}
