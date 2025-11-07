using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Entities.Models;

namespace Application.Abstractions.Interfaces
{
    public interface IAdminCodeRepository
    {
        Task<AdminCode> GetByCodeAsync(string code);
        Task<AdminCode> AddAsync(AdminCode adminCode);
        Task MarkAsUsedAsync(int id, int userId);
        Task<List<AdminCode>> GetAllAsync();
        Task<List<AdminCode>> GetUnusedAsync();
    }
}
