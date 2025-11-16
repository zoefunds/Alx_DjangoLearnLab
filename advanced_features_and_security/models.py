from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone


class Author(models.Model):
    """Model to represent book authors."""
    name = models.CharField(max_length=200, unique=True)
    bio = models.TextField(blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    nationality = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Authors'
        indexes = [
            models.Index(fields=['name']),
        ]

    def __str__(self):
        return self.name


class Category(models.Model):
    """Model to represent book categories."""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Publisher(models.Model):
    """Model to represent book publishers."""
    name = models.CharField(max_length=200, unique=True)
    address = models.TextField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    website = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Book(models.Model):
    """Model to represent books in the library."""
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('borrowed', 'Borrowed'),
        ('reserved', 'Reserved'),
        ('damaged', 'Damaged'),
    ]

    title = models.CharField(max_length=300)
    isbn = models.CharField(max_length=13, unique=True)
    description = models.TextField(blank=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='books')
    publisher = models.ForeignKey(Publisher, on_delete=models.SET_NULL, null=True, blank=True, related_name='books')
    publication_date = models.DateField()
    pages = models.IntegerField(validators=[MinValueValidator(1)])
    language = models.CharField(max_length=50, default='English')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    quantity = models.IntegerField(default=1, validators=[MinValueValidator(0)])
    available_copies = models.IntegerField(default=1, validators=[MinValueValidator(0)])
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0, validators=[MinValueValidator(0), MaxValueValidator(5)])
    cover_image = models.ImageField(upload_to='book_covers/%Y/%m/%d/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Books'
        indexes = [
            models.Index(fields=['isbn']),
            models.Index(fields=['title']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return f"{self.title} by {self.author.name}"

    def is_available(self):
        """Check if book has available copies."""
        return self.available_copies > 0


class Borrowing(models.Model):
    """Model to track book borrowing history."""
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='borrowings')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='borrowings')
    borrowed_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField()
    return_date = models.DateField(blank=True, null=True)
    is_returned = models.BooleanField(default=False)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-borrowed_date']
        verbose_name_plural = 'Borrowings'
        indexes = [
            models.Index(fields=['user', 'is_returned']),
            models.Index(fields=['book', 'is_returned']),
        ]

    def __str__(self):
        return f"{self.user.username} borrowed {self.book.title}"

    def is_overdue(self):
        """Check if the borrowed book is overdue."""
        if not self.is_returned:
            return timezone.now().date() > self.due_date
        return False


class Reservation(models.Model):
    """Model to track book reservations."""
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reservations')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reservations')
    reservation_date = models.DateTimeField(auto_now_add=True)
    expiry_date = models.DateField()
    is_active = models.BooleanField(default=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-reservation_date']
        verbose_name_plural = 'Reservations'
        indexes = [
            models.Index(fields=['user', 'is_active']),
            models.Index(fields=['book', 'is_active']),
        ]

    def __str__(self):
        return f"{self.user.username} reserved {self.book.title}"

    def is_expired(self):
        """Check if reservation has expired."""
        return timezone.now().date() > self.expiry_date and self.is_active


class Review(models.Model):
    """Model for book reviews and ratings."""
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    title = models.CharField(max_length=200)
    content = models.TextField()
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    helpful_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Reviews'
        unique_together = ['book', 'user']
        indexes = [
            models.Index(fields=['book', '-created_at']),
            models.Index(fields=['user', '-created_at']),
        ]

    def __str__(self):
        return f"Review by {self.user.username} for {self.book.title}"


class Wishlist(models.Model):
    """Model for user wishlists."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlist')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='wishlisted_by')
    added_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-added_date']
        verbose_name_plural = 'Wishlists'
        unique_together = ['user', 'book']
        indexes = [
            models.Index(fields=['user', '-added_date']),
        ]

    def __str__(self):
        return f"{self.user.username}'s wishlist - {self.book.title}"