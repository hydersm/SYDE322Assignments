drop table if exists hotels;
create table hotels (
  hotelId integer,
  hotelName text not null,
  city text not null,
  primary key (hotelID)
);

drop table if exists rooms;
create table rooms (
  hotelId integer not null,
  roomNo integer,
  price single not null,
  type text not null,
  primary key (roomNo),
  foreign key (hotelId) references hotels(hotelID) on delete cascade on update cascade
);

drop table if exists guests;
create table guests (
  guestId integer,
  guestName text not null,
  guestAddress text not null,
  primary key (guestId)
);

drop table if exists bookings;
create table bookings (
  hotelId integer not null,
  roomNo integer not null,
  guestId integer not null,
  bookingId integer,
  startDate date not null,
  endDate date not null,
  primary key (bookingId),
  foreign key (hotelId) references hotels(hotelId) on delete cascade on update cascade,
  foreign key (roomNo) references rooms(roomNo) on delete cascade on update cascade,
  foreign key (guestId) references guests(guestId) on delete cascade on update cascade
);
