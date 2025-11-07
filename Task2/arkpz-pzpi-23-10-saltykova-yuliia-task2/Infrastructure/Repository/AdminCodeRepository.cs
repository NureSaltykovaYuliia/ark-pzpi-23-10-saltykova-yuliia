using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Application.Abstractions.Interfaces;
using Entities.Models;
using Microsoft.EntityFrameworkCore;

namespace Infrastructure.Repositories
{
    public class AdminCodeRepository : IAdminCodeRepository
    {
        private readonly MyDbContext _context;

        public AdminCodeRepository(MyDbContext context)
        {
            _context = context;
        }

        public async Task<AdminCode> GetByCodeAsync(string code)
        {
            return await _context.AdminCodes
                .FirstOrDefaultAsync(ac => ac.Code == code);
        }

        public async Task<AdminCode> AddAsync(AdminCode adminCode)
        {
            _context.AdminCodes.Add(adminCode);
            await _context.SaveChangesAsync();
            return adminCode;
        }

        public async Task MarkAsUsedAsync(int id, int userId)
        {
            var adminCode = await _context.AdminCodes.FindAsync(id);
            if (adminCode != null)
            {
                adminCode.IsUsed = true;
                adminCode.UsedAt = DateTime.UtcNow;
                adminCode.UsedByUserId = userId;
                await _context.SaveChangesAsync();
            }
        }

        public async Task<List<AdminCode>> GetAllAsync()
        {
            return await _context.AdminCodes
                .Include(ac => ac.UsedBy)
                .OrderByDescending(ac => ac.CreatedAt)
                .ToListAsync();
        }

        public async Task<List<AdminCode>> GetUnusedAsync()
        {
            return await _context.AdminCodes
                .Where(ac => !ac.IsUsed)
                .OrderByDescending(ac => ac.CreatedAt)
                .ToListAsync();
        }
    }
}
