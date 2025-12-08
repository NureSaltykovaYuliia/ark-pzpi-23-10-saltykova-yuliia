using Application.Abstractions.Interfaces;
using Entities.Models;
using Infrastructure; 
using Microsoft.EntityFrameworkCore;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace Infrastructure.Repositories
{
    public class MessageRepository : IMessageRepository
    {
        private readonly MyDbContext _context;

        public MessageRepository(MyDbContext context)
        {
            _context = context;
        }

        public async Task<Message> CreateMessageAsync(Message message)
        {
            // 1. Додаємо повідомлення
            await _context.Messages.AddAsync(message);
            await _context.SaveChangesAsync();

            // 2. Перезавантажуємо повідомлення з даними про відправника
            // Це потрібно, щоб ChatHub міг відправити повний об'єкт (з ім'ям відправника) іншим клієнтам
            return await _context.Messages
                .Include(m => m.Sender)
                .FirstAsync(m => m.Id == message.Id);
        }

        public async Task<IEnumerable<Message>> GetMessagesAsync(int conversationId, int count)
        {
            // Завантажуємо останні N повідомлень для конкретної розмови
            return await _context.Messages
                .Include(m => m.Sender) // Включаємо відправника, щоб знати, хто написав
                .Where(m => m.ConversationId == conversationId)
                .OrderByDescending(m => m.Timestamp) // Спочатку беремо найновіші
                .Take(count)
                .OrderBy(m => m.Timestamp) // Потім сортуємо їх у правильному порядку (старі -> нові)
                .ToListAsync();
        }
    }
}
