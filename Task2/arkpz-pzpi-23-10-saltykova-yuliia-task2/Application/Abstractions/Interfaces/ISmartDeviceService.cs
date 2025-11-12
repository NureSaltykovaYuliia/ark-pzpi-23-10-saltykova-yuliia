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
    }
}
