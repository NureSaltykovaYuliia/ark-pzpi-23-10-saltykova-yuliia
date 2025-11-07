using Application.DTOs;

namespace Application.Abstractions.Interfaces
{
    public interface IEventService
    {
        Task<IEnumerable<EventDto>> GetAllEventsAsync();
        Task<IEnumerable<EventDto>> GetUpcomingEventsAsync();
        Task<IEnumerable<EventDto>> GetEventsByOrganizerIdAsync(int organizerId);
        Task<EventDto?> GetEventByIdAsync(int id);
        Task<EventDto> CreateEventAsync(CreateUpdateEventDto eventDto, int organizerId);
        Task UpdateEventAsync(int id, CreateUpdateEventDto eventDto, int organizerId);
        Task DeleteEventAsync(int id, int organizerId);
    }
}
