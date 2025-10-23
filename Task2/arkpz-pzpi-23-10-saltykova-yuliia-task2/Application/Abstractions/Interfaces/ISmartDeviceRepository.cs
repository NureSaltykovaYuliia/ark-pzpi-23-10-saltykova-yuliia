using Entities.Models;

namespace Application.Abstractions.Interfaces
{
    public interface ISmartDeviceRepository
    {
        Task<SmartDevice?> GetByIdAsync(int deviceId);
        Task<SmartDevice?> GetByDogIdAsync(int dogId);
        Task<SmartDevice?> GetByDeviceGuidAsync(string deviceGuid);
        Task<IEnumerable<SmartDevice>> GetAllAsync();
        Task<SmartDevice> AddAsync(SmartDevice device);
        Task UpdateAsync(SmartDevice device);
        Task DeleteAsync(int deviceId);
    }
}
