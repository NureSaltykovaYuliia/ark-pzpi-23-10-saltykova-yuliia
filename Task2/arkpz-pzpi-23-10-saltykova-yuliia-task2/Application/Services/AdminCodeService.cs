using Application.Abstractions.Interfaces;
using Application.DTOs;
using Entities.Models;

namespace Application.Services
{
    public class AdminCodeService : IAdminCodeService
    {
        private readonly IAdminCodeRepository _adminCodeRepository;

        public AdminCodeService(IAdminCodeRepository adminCodeRepository)
        {
            _adminCodeRepository = adminCodeRepository;
        }

        public async Task<AdminCodeDto> CreateAdminCodeAsync()
        {
            var adminCode = new AdminCode
            {
                Code = GenerateUniqueCode(),
                IsUsed = false,
                CreatedAt = DateTime.UtcNow
            };

            var createdCode = await _adminCodeRepository.AddAsync(adminCode);
            return MapToDto(createdCode);
        }

        public async Task<IEnumerable<AdminCodeDto>> GetAllAdminCodesAsync()
        {
            var codes = await _adminCodeRepository.GetAllAsync();
            return codes.Select(MapToDto);
        }

        public async Task<IEnumerable<AdminCodeDto>> GetUnusedAdminCodesAsync()
        {
            var codes = await _adminCodeRepository.GetUnusedAsync();
            return codes.Select(MapToDto);
        }

        public async Task<AdminCodeDto> CreateFirstAdminCodeAsync()
        {
            var existingCodes = await _adminCodeRepository.GetAllAsync();
            if (existingCodes.Count > 0)
                throw new Exception("Коди адміністратора вже існують. Використовуйте звичайний endpoint.");

            var adminCode = new AdminCode
            {
                Code = GenerateUniqueCode(),
                IsUsed = false,
                CreatedAt = DateTime.UtcNow
            };

            var createdCode = await _adminCodeRepository.AddAsync(adminCode);
            return MapToDto(createdCode);
        }

        private static string GenerateUniqueCode()
        {
            return Guid.NewGuid().ToString("N").Substring(0, 16).ToUpper();
        }

        private static AdminCodeDto MapToDto(AdminCode ac)
        {
            return new AdminCodeDto
            {
                Id = ac.Id,
                Code = ac.Code,
                IsUsed = ac.IsUsed,
                CreatedAt = ac.CreatedAt,
                UsedAt = ac.UsedAt,
                UsedByUserId = ac.UsedByUserId,
                UsedByUsername = ac.UsedBy?.Username
            };
        }
    }
}
