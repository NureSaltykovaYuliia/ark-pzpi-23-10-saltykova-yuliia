using Application.Abstractions.Interfaces;
using Application.DTOs;
using Entities.Models;

namespace Application.Services
{
    public class SmartDeviceService : ISmartDeviceService
    {
        private readonly ISmartDeviceRepository _deviceRepository;
        private readonly IDogRepository _dogRepository;

        public SmartDeviceService(ISmartDeviceRepository deviceRepository, IDogRepository dogRepository)
        {
            _deviceRepository = deviceRepository;
            _dogRepository = dogRepository;
        }

        public async Task<IEnumerable<SmartDeviceDto>> GetAllDevicesAsync(int userId, string userRole)
        {
            IEnumerable<SmartDevice> devices;

            // Якщо користувач - адміністратор, показуємо всі пристрої
            if (userRole == "Admin")
            {
                devices = await _deviceRepository.GetAllAsync();
            }
            else
            {
                // Інакше показуємо тільки пристрої собак цього користувача
                devices = await _deviceRepository.GetByUserIdAsync(userId);
            }

            return devices.Select(d => MapToDto(d));
        }

        public async Task<SmartDeviceDto?> GetDeviceByIdAsync(int id, int userId)
        {
            var device = await _deviceRepository.GetByIdAsync(id);
            if (device == null) return null;

            var dog = await _dogRepository.GetByIdAsync(device.DogId);
            if (dog != null && dog.OwnerId != userId)
                throw new UnauthorizedAccessException("Ви не маєте доступу до цього пристрою");

            return MapToDto(device);
        }

        public async Task<SmartDeviceDto?> GetDeviceByDogIdAsync(int dogId, int userId)
        {
            var dog = await _dogRepository.GetByIdAsync(dogId);
            if (dog == null)
                throw new Exception("Собака не знайдена");

            if (dog.OwnerId != userId)
                throw new UnauthorizedAccessException("Ви не маєте доступу до цієї собаки");

            var device = await _deviceRepository.GetByDogIdAsync(dogId);
            if (device == null) return null;

            return MapToDto(device);
        }

        public async Task<SmartDeviceDto> CreateDeviceAsync(CreateSmartDeviceDto deviceDto, int userId)
        {
            var dog = await _dogRepository.GetByIdAsync(deviceDto.DogId);
            if (dog == null)
                throw new Exception("Собака не знайдена");

            if (dog.OwnerId != userId)
                throw new UnauthorizedAccessException("Ви не маєте доступу до цієї собаки");

            var existingDevice = await _deviceRepository.GetByDogIdAsync(deviceDto.DogId);
            if (existingDevice != null)
                throw new Exception("До цієї собаки вже прикріплений пристрій");

            var device = new SmartDevice
            {
                DeviceGuid = deviceDto.DeviceGuid,
                DogId = deviceDto.DogId,
                LastLatitude = 0,
                LastLongitude = 0,
                BatteryLevel = 100
            };

            var createdDevice = await _deviceRepository.AddAsync(device);
            return MapToDto(createdDevice, dog.Name);
        }

        public async Task UpdateDeviceAsync(int id, UpdateSmartDeviceDto deviceDto, int userId)
        {
            var device = await _deviceRepository.GetByIdAsync(id);
            if (device == null)
                throw new Exception("Пристрій не знайдено");

            var dog = await _dogRepository.GetByIdAsync(device.DogId);
            if (dog != null && dog.OwnerId != userId)
                throw new UnauthorizedAccessException("Ви не маєте доступу до цього пристрою");

            device.LastLatitude = deviceDto.LastLatitude;
            device.LastLongitude = deviceDto.LastLongitude;
            device.BatteryLevel = deviceDto.BatteryLevel;

            await _deviceRepository.UpdateAsync(device);
        }

        public async Task DeleteDeviceAsync(int id, int userId)
        {
            var device = await _deviceRepository.GetByIdAsync(id);
            if (device == null)
                throw new Exception("Пристрій не знайдено");

            var dog = await _dogRepository.GetByIdAsync(device.DogId);
            if (dog != null && dog.OwnerId != userId)
                throw new UnauthorizedAccessException("Ви не маєте доступу до цього пристрою");

            await _deviceRepository.DeleteAsync(id);
        }

        private static SmartDeviceDto MapToDto(SmartDevice d, string? dogName = null)
        {
            return new SmartDeviceDto
            {
                Id = d.Id,
                DeviceGuid = d.DeviceGuid,
                LastLatitude = d.LastLatitude,
                LastLongitude = d.LastLongitude,
                BatteryLevel = d.BatteryLevel,
                DogId = d.DogId,
                DogName = dogName ?? d.Dog?.Name
            };
        }
    }
}
