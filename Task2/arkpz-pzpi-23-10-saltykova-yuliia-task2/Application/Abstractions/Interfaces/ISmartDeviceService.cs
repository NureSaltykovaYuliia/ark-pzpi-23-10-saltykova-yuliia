using Application.DTOs;

namespace Application.Abstractions.Interfaces
{
    public interface ISmartDeviceService
    {
        Task<IEnumerable<SmartDeviceDto>> GetAllDevicesAsync(int userId, string userRole);
        Task<SmartDeviceDto?> GetDeviceByIdAsync(int id, int userId);
        Task<SmartDeviceDto?> GetDeviceByDogIdAsync(int dogId, int userId);
        Task<SmartDeviceDto> CreateDeviceAsync(CreateSmartDeviceDto deviceDto, int userId);
        Task UpdateDeviceAsync(int id, UpdateSmartDeviceDto deviceDto, int userId);
        Task DeleteDeviceAsync(int id, int userId);

        // Методи для роботи пристрою (без авторизації)
        Task<SmartDeviceDto> RegisterDeviceAsync(string deviceGuid);
        Task<int?> GetDogIdByDeviceGuidAsync(string deviceGuid);
        Task UpdateDeviceTelemetryAsync(int id, UpdateSmartDeviceDto deviceDto);

        // Метод для прив'язки пристрою до собаки (з авторизацією)
        Task AssignDeviceToDogAsync(string deviceGuid, int dogId, int userId);
    }
}
