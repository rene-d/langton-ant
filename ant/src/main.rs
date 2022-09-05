//! Langton's ant

use std::collections::HashSet;
use std::{thread, time};

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
struct Position {
    x: i32,
    y: i32,
}

struct Game {
    black: HashSet<Position>,
    direction: char,
    position: Position,
    pos_ll: Position,
    pos_ur: Position,
}

impl Game {
    fn step(&mut self) {
        if self.black.contains(&self.position) {
            self.direction = turn_right(self.direction);
            self.black.remove(&self.position);
        } else {
            self.direction = turn_left(self.direction);
            self.black.insert(self.position);
        }

        move_ant(&mut self.position, self.direction);

        if self.position.x > self.pos_ur.x {
            self.pos_ur.x = self.position.x;
        }
        if self.position.y > self.pos_ur.y {
            self.pos_ur.y = self.position.y;
        }
        if self.position.x < self.pos_ll.x {
            self.pos_ll.x = self.position.x;
        }
        if self.position.y < self.pos_ll.y {
            self.pos_ll.y = self.position.y;
        }
    }

    fn show(&self) {
        print!("\x1B[H\x1B[2J\x1B[3J");
        println!(
            "current: {:?}   direction: {}   box: {:?} {:?}",
            self.position, self.direction, self.pos_ll, self.pos_ur
        );
        for y in (self.pos_ll.y..=self.pos_ur.y).rev() {
            for x in (self.pos_ll.x..=self.pos_ur.x).rev() {
                let pos = Position { x: x, y: y };
                if self.black.contains(&pos) {
                    print!("#");
                } else {
                    print!(" ");
                }
            }
            println!();
        }
    }
}

/// Turn the ant right
fn turn_right(direction: char) -> char {
    match direction {
        'W' => 'N',
        'N' => 'E',
        'E' => 'S',
        'S' => 'W',
        _ => panic!("not a direction"),
    }
}

fn turn_left(direction: char) -> char {
    match direction {
        'W' => 'S',
        'S' => 'E',
        'E' => 'N',
        'N' => 'W',
        _ => panic!("not a direction"),
    }
}

fn move_ant(position: &mut Position, direction: char) {
    match direction {
        'E' => position.x += 1,
        'S' => position.y -= 1,
        'W' => position.x -= 1,
        'N' => position.y += 1,
        _ => panic!("not a direction"),
    }
}

fn main() {
    let mut game = Game {
        black: HashSet::new(),
        direction: 'E',
        position: Position { x: 0, y: 0 },
        pos_ll: Position { x: 0, y: 0 },
        pos_ur: Position { x: 22, y: 29 },
    };

    for i in 0..11500 {
        game.step();

        if i % 1000 == 0 {
            game.show();

            let ten_millis = time::Duration::from_millis(100);
            thread::sleep(ten_millis);
        }
    }
}
