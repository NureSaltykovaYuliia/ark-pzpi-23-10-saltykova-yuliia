using Entities.Models;

namespace Application.Abstractions.Interfaces
{
    public interface IEventRepository
    {
        Task<Event?> GetByIdAsync(int eventId);
        Task<IEnumerable<Event>> GetAllAsync();
        Task<IEnumerable<Event>> GetByOrganizerIdAsync(int organizerId);
        Task<IEnumerable<Event>> GetUpcomingEventsAsync();
        Task<Event> AddAsync(Event eventEntity);
        Task UpdateAsync(Event eventEntity);
        Task DeleteAsync(int eventId);
    }
}
