using System;

namespace Application.DTOs
{
    public class UpdateUserProfileDto
    {
        public string? Username { get; set; }
        public string? Bio { get; set; }
        public double? LastLatitude { get; set; }
        public double? LastLongitude { get; set; }
    }
}
