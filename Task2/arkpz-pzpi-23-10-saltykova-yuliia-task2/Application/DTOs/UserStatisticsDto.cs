using System;

namespace Application.DTOs
{
    public class UserStatisticsDto
    {
        public int TotalUsers { get; set; }           // Загальна кількість користувачів
        public int ActiveUsers { get; set; }          // Активні за останні 30 днів
        public int BlockedUsers { get; set; }         // Заблоковані користувачі
        public int TotalRegularUsers { get; set; }    // Звичайні користувачі (DogOwner)
        public int TotalAdmins { get; set; }          // Адміністратори
    }
}
