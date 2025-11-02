using Entities.Models;

public interface IConversationRepository
{
    Task<IEnumerable<Conversation>> GetUserConversationsAsync(int userId);
    Task<Conversation?> FindPrivateConversationAsync(int user1Id, int user2Id);
    Task<Conversation> CreateConversationAsync(Conversation conversation);
    Task<Conversation?> GetByIdAsync(int conversationId);
}