using Application.Abstractions.Interfaces;
using Entities.Models;
using Infrastructure;
using Microsoft.EntityFrameworkCore;

namespace Infrastructure.Repositories
{
    public class SmartDeviceRepository : ISmartDeviceRepository
    {
        private readonly MyDbContext _context;

        public SmartDeviceRepository(MyDbContext context)
        {
            _context = context;
        }

        public async Task<SmartDevice?> GetByIdAsync(int deviceId)
        {
            return await _context.SmartDevices
                .Include(sd => sd.Dog)
                .FirstOrDefaultAsync(sd => sd.Id == deviceId);
        }

        public async Task<SmartDevice?> GetByDogIdAsync(int dogId)
        {
            return await _context.SmartDevices
                .Include(sd => sd.Dog)
                .FirstOrDefaultAsync(sd => sd.DogId == dogId);
        }

        public async Task<SmartDevice?> GetByDeviceGuidAsync(string deviceGuid)
        {
            return await _context.SmartDevices
                .Include(sd => sd.Dog)
                .FirstOrDefaultAsync(sd => sd.DeviceGuid == deviceGuid);
        }

        public async Task<IEnumerable<SmartDevice>> GetAllAsync()
        {
            return await _context.SmartDevices
                .Include(sd => sd.Dog)
                .ToListAsync();
        }

        public async Task<SmartDevice> AddAsync(SmartDevice device)
        {
            _context.SmartDevices.Add(device);
            await _context.SaveChangesAsync();
            return device;
        }

        public async Task UpdateAsync(SmartDevice device)
        {
            _context.SmartDevices.Update(device);
            await _context.SaveChangesAsync();
        }

        public async Task DeleteAsync(int deviceId)
        {
            var device = await GetByIdAsync(deviceId);
            if (device != null)
            {
                _context.SmartDevices.Remove(device);
                await _context.SaveChangesAsync();
            }
        }
    }
}
