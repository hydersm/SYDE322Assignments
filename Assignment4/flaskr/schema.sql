create table hotels (
  hotelId integer primary key autoincrement,
  hotelName text not null,
  city text not null
);

create table rooms (
  roomNo integer primary key autoincrement,
  hotelId integer not null,
  title text not null,
  text text not null
);

create table guests (
  guestId integer primary key autoincrement,
  guestName text not null,
  guestAddress text not null
);

create table bookings (
  bookingId integer primary key autoincrement,
  guestId integer not null,
  hotelId integer not null,
  startDate text not null,
  endDate text not null
);