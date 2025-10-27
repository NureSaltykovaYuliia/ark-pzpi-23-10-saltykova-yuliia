<? php
/* ===== В.1 ===== */

// Приклад хорошого коду 
namespace MyProject\Repository;

use MyProject\Database\Connection;

class UserRepository
 {
    // …
 }

// Приклад поганого коду 
require_once 'db.php';
require_once 'user.php';

$db_connection = connect_to_db();
$user_data = get_user($db_connection, 1);

/* ===== В.2 ===== */

// Приклад поганого коментаря

// Збільшуємо лічильник на 1
$i++;

// Приклад хорошого коментаря

// Запускаємо перерахунок кешу після оновлення профілю,
// щоб користувач одразу побачив зміни.
$cache->recalculate();

/* ===== В.3 ===== */

// Погане іменування
$user_data = ['name' => 'Alex']; // snake_case для змінної
const records_limit = 50; // нижній регістр для константи

class user_service // нижній регістр для класу
{

  public function GetUserData() // PascalCase для методу
  {
   // ...
  }

}

// Гарне іменування
$userData = ['name' => 'Alex']; // camelCase для змінної
const RECORDS_LIMIT = 50; // SCREAMING_SNAKE_CASE для константи

class UserService // UpperCamelCase для класу
{

public function getUserData() : array // camelCase для методу
  {
     // ...
  }
}

/* ===== В.4 ===== */

// Погане іменування
$user_data = ['name' => 'Alex']; // snake_case для змінної
const records_limit = 50; // нижній регістр для константи

class user_service // нижній регістр для класу
{

   public function GetUserData() // PascalCase для методу
   {
      // ...
   }
}

// Гарне іменування
$userData = ['name' => 'Alex']; // camelCase для змінної
const RECORDS_LIMIT = 50; // SCREAMING_SNAKE_CASE для константи

class UserService // UpperCamelCase для класу
{
  
   public function getUserData(): array // camelCase для методу
   {

   }
}

/* ===== В.5 ===== */

// Приклад поганого коду 
function calculateOrderTotal(int $quantity, int $userStatus): float
{
   $price = 9.99; // Що це за ціна?
   $total = $quantity * $price;

   // 3 - це статус преміум-користувача?
   if ($userStatus === 3) {
   $total *= 0.9; // 10% знижка
   }
   return $total;
} 

// Приклад хорошого коду  
class OrderCalculator
{

   private const BASE_PRICE = 9.99;
   private const PREMIUM_USER_STATUS = 3;
   private const PREMIUM_DISCOUNT = 0.9;

   public function calculateTotal(int $quantity, int $userStatus): float
   {

      $total = $quantity * self: :BASE_PRICE;

      if ($userStatus === self: :PREMIUM_USER_STATUS) {
      $total *= self :: PREMIUM_DISCOUNT;

      }

   return $total;

   }
}

/* ===== В.6 ===== */

// Приклад поганого коду 
function findUsers($search, $limit, $activeOnly)
{

// якийсь код для пошуку

return []; // що повертається? масив чого?

}

// Приклад хорошого коду  
/**
* Знаходить користувачів за заданим критерієм пошуку.
*
* @param string $search Рядок для пошуку (наприклад, ім'я або email).
* @param int $limit Максимальна кількість користувачів для повернення
* @param bool $activeOnly Повертати тільки активних користувачів
*
* @return User[] Масив об'єктів User.
*/

function findUsers(string $search, int $limit, bool $activeOnly): array
{
// ... логіка пошуку
return [];

}

/* ===== В.7 ===== */

// Спочатку тест
public function test_adds_two_numbers()
{
   $calculator = new Calculator();
   $result = $calculator->add(2, 3);
   $this->assertEquals(5, $result);
}

// Потім код
class Calculator
{
   public function add(int $a, int $b): int
   {
     return $a + $b;
   }
}