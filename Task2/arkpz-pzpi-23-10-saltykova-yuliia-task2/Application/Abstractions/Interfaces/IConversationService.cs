using Application.DTOs;

namespace Application.Abstractions.Interfaces
{
    public interface IConversationService
    {
        Task<IEnumerable<ConversationDto>> GetUserConversationsAsync(int userId);
        Task<IEnumerable<MessageDto>> GetMessageHistoryAsync(int conversationId, int count = 50);
    }
}
