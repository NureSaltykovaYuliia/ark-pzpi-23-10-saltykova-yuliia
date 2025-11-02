using Entities.Models;

public interface IMessageRepository
{
    Task<IEnumerable<Message>> GetMessagesAsync(int conversationId, int count);
    Task<Message> CreateMessageAsync(Message message);
}