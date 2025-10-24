
-- 1. T?O B?NG 'users'
CREATE TABLE users (
    -- D�ng UNIQUEIDENTIFIER l�m ki?u d? li?u cho ID, v� ??t gi� tr? m?c ??nh l� m?t UUID m?i
    id UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),

    -- D�ng NVARCHAR ?? h? tr? t?t c�c k� t? Unicode (nh? ti?ng Vi?t)
    email NVARCHAR(255) NOT NULL UNIQUE,
    password_hash NVARCHAR(255) NOT NULL,
    full_name NVARCHAR(255),
    phone_number NVARCHAR(20) UNIQUE,

    -- Thay th? cho ENUM c?a MySQL: D�ng NVARCHAR v� m?t r�ng bu?c CHECK
    -- ?? ??m b?o gi� tr? ch? c� th? l� 'passenger' ho?c 'driver'
    user_type NVARCHAR(10) NOT NULL CHECK (user_type IN ('passenger', 'driver')),

    -- D�ng DATETIME2 l� ki?u d? li?u ng�y gi? ti�u chu?n, ch�nh x�c cao
    created_at DATETIME2 DEFAULT GETDATE(),
    updated_at DATETIME2 DEFAULT GETDATE()
);
GO -- D?u ng?t l?nh trong T-SQL

-- 2. T?O TRIGGER ?? T? ??NG C?P NH?T TR??NG 'updated_at'
CREATE TRIGGER trg_users_update_timestamp
ON users          -- Trigger n�y �p d?ng cho b?ng 'users'
AFTER UPDATE      -- N� s? ???c k�ch ho?t SAU KHI c� l?nh UPDATE
AS
BEGIN
    -- C?p nh?t c?t 'updated_at' th�nh th?i gian hi?n t?i
    -- cho t?t c? c�c d�ng v?a ???c thay ??i (n?m trong b?ng t?m 'inserted')
    UPDATE u
    SET updated_at = GETDATE()
    FROM users u
    INNER JOIN inserted i ON u.id = i.id;
END;
GO

PRINT 'B?ng "users" v� trigger "trg_users_update_timestamp" ?� ???c t?o th�nh c�ng!';
SELECT * FROM users;