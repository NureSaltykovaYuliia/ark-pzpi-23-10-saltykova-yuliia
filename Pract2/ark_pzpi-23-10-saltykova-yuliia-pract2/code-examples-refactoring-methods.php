<?php

/*=====В.1 Push Down Method до рефакторингу===== */

abstract class User
{
    protected string $username;

    public function __construct(string $username)
    {
        $this->username = $username;
    }

    public function login()
    {
        echo "Користувач {$this->username} увійшов в систему.\n";
    }
    public function banUser(User $otherUser)
    {
        if ($this instanceof Admin) {
            echo "Адмін {$this->username} заблокував користувача {$otherUser->username}.\n";
        } else {

            throw new \Exception("Тільки адміни можуть блокувати користувачів!");
        }
    }
}

class StandardUser extends User
{
    public function postComment()
    {
        echo "{$this->username} опублікував коментар.\n";
    }
}

class Admin extends User
{
    public function manageSystem()
    {
        echo "{$this->username} керує системою.\n";
    }
}
?>

<?php
/*=====В.2 Push Down Method після рефакторингу===== */
abstract class User
{
    public string $username;

    public function __construct(string $username)
    {
        $this->username = $username;
    }

    public function login()
    {
        echo "Користувач {$this->username} увійшов в систему.\n";
    }
}

class StandardUser extends User
{
    public function postComment()
    {
        echo "{$this->username} опублікував коментар.\n";
    }
}

class Admin extends User
{
    public function banUser(User $otherUser)
    {
        echo "Адмін {$this->username} заблокував користувача {$otherUser->username}.\n";
    }

    public function manageSystem()
    {
        echo "{$this->username} керує системою.\n";
    }
}
?>


<?php
/*=====В.3 Self Encapsulate Field до рефакторингу===== */
class Product
{
    private float $price;
    private string $name;

    public function __construct(string $name, float $price)
    {
        $this->name = $name;
        if ($price < 0) {
            $this->price = 0;
        } else {
            $this->price = $price;
        }
    }

    public function getFormattedPrice(): string
    {
        return '$' . number_format($this->price, 2);
    }
}
?>

<?php
/*=====В.4 Self Encapsulate Field після рефакторингу===== */
class Product
{
    private float $price;
    private string $name;

    public function __construct(string $name, float $price)
    {
        $this->name = $name;
        $this->setPrice($price);
    }

    public function getFormattedPrice(): string
    {
        return '$' . number_format($this->getPrice(), 2);
    }

    private function setPrice(float $price): void
    {
        if ($price < 0) {
            $this->price = 0;
        } else {
            $this->price = $price;
        }
    }

    private function getPrice(): float
    {
        return $this->price;
    }
}
?>

<?php
/*=====В.5 Consolidate Duplicate Conditional Fragments до рефакторингу===== */
class Order1
{
    private float $totalPrice;

    public function calculateShipping(string $country)
    {
        $shippingCost = 0;

        if ($country === 'USA') {
            $shippingCost = 10.00;
            $this->totalPrice += $shippingCost;
            $this->sendNotification("Вартість доставки: $shippingCost");
        } else {
            $shippingCost = 25.00;
            $this->totalPrice += $shippingCost;
            $this->sendNotification("Вартість доставки: $shippingCost");
        }
    }

    // ...
    private function sendNotification(string $message) { /* ... */ }
}
?>

<?php
/*=====В.6 Consolidate Duplicate Conditional Fragments після рефакторингу===== */
class Order
{
    private float $totalPrice;

    public function calculateShipping(string $country)
    {
        $shippingCost = 0;

        if ($country === 'USA') {
            $shippingCost = 10.00;
        } else {
            $shippingCost = 25.00;
        }

        $this->totalPrice += $shippingCost;
        $this->sendNotification("Вартість доставки: $shippingCost");
    }

    // ...
    private function sendNotification(string $message) { /* ... */ }
}
?>