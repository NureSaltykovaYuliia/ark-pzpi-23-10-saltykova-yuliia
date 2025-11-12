using System;
using Entities.Models;

namespace Application.DTOs
{
    public class UserProfileDto
    {
        public int Id { get; set; }
        public string Username { get; set; }
        public string Email { get; set; }
        public string Bio { get; set; }
        public UserRole Role { get; set; }
        public double? LastLatitude { get; set; }
        public double? LastLongitude { get; set; }
        public DateTime? LastActivity { get; set; }
        public bool IsBlocked { get; set; }
        public string? BlockReason { get; set; }
    }
}
