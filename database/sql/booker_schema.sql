DROP TABLE IF EXISTS Booking;
DROP TABLE IF EXISTS Room;


CREATE TABLE Room (
    R_ID            INTEGER PRIMARY KEY,
    R_RoomNumber    TEXT,
    R_Name          TEXT
);

CREATE TABLE Booking (
    B_StartDate     TEXT,
    B_EndDate       TEXT,
    B_UserID        TEXT,
    B_Name          TEXT,
    B_RoomID        INTEGER,

    PRIMARY KEY(B_UserID, B_StartDate, B_EndDate, B_RoomID)
    FOREIGN KEY(B_RoomID) REFERENCES Room(R_ID)
);
