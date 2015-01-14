/*--------------------------------------------------------------------------
    Pawny 0.3.1, chess engine (source code).
    Copyright (C) 2009 - 2011 by Mincho Georgiev.
    
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
    
    contact: pawnychess@gmail.com 
    web: http://www.pawny.netii.net/
----------------------------------------------------------------------------*/
#include "data.h"

const int square_color[128] = 
{
    1,  0,  1,  0,  1,  0,  1,  0,  0,0,0,0,0,0,0,0,
    0,  1,  0,  1,  0,  1,  0,  1,  0,0,0,0,0,0,0,0,
    1,  0,  1,  0,  1,  0,  1,  0,  0,0,0,0,0,0,0,0,
    0,  1,  0,  1,  0,  1,  0,  1,  0,0,0,0,0,0,0,0,
    1,  0,  1,  0,  1,  0,  1,  0,  0,0,0,0,0,0,0,0,
    0,  1,  0,  1,  0,  1,  0,  1,  0,0,0,0,0,0,0,0,
    1,  0,  1,  0,  1,  0,  1,  0,  0,0,0,0,0,0,0,0,
    0,  1,  0,  1,  0,  1,  0,  1,  0,0,0,0,0,0,0,0
};

const int psq_outposts[2][128] = 
{	
  {
    0,  0,  0,  0,  0,  0,  0,  0,  0,0,0,0,0,0,0,0,
    0,  0,  0,  0,  0,  0,  0,  0,  0,0,0,0,0,0,0,0,
    0,  0,  0,  0,  0,  0,  0,  0,  0,0,0,0,0,0,0,0,
    0,  2,  6, 10, 10,  6,  2,  0,  0,0,0,0,0,0,0,0,
    0,  2,  6, 12, 12,  6,  2,  0,  0,0,0,0,0,0,0,0,
    0,  4,  4,  6,  6,  4,  4,  0,  0,0,0,0,0,0,0,0,
    0,  0,  0,  0,  0,  0,  0,  0,  0,0,0,0,0,0,0,0,
    0,  0,  0,  0,  0,  0,  0,  0,  0,0,0,0,0,0,0,0
  },
  {
    0,  0,  0,  0,  0,  0,  0,  0,  0,0,0,0,0,0,0,0,
    0,  0,  0,  0,  0,  0,  0,  0,  0,0,0,0,0,0,0,0,
    0,  4,  4,  6,  6,  4,  4,  0,  0,0,0,0,0,0,0,0,
    0,  2,  6, 12, 12,  6,  2,  0,  0,0,0,0,0,0,0,0,
    0,  2,  6, 10, 10,  6,  2,  0,  0,0,0,0,0,0,0,0,
    0,  0,  0,  0,  0,  0,  0,  0,  0,0,0,0,0,0,0,0,
    0,  0,  0,  0,  0,  0,  0,  0,  0,0,0,0,0,0,0,0,
    0,  0,  0,  0,  0,  0,  0,  0,  0,0,0,0,0,0,0,0
  }
};

const int psq_table[15][128] = 
{
  //empty
  {0},
  
  //white pawn
  {	
      0,  0,  0,  0,  0,  0,  0,  0,  0,0,0,0,0,0,0,0,
      0,  0,  0,-12,-12,  0,  0,  0,  0,0,0,0,0,0,0,0,
      0,  0,  0,  4,  4,  0,  0,  0,  0,0,0,0,0,0,0,0,
      0,  4,  4, 16, 16,  4,  4,  0,  0,0,0,0,0,0,0,0,
      4, 12, 12, 14, 14, 12, 12,  4,  0,0,0,0,0,0,0,0,
     12, 20, 20, 25, 25, 20, 20, 12,  0,0,0,0,0,0,0,0,
     65, 80, 85, 90, 90, 85, 80, 65,  0,0,0,0,0,0,0,0,
      0,  0,  0,  0,  0,  0,  0,  0,  0,0,0,0,0,0,0,0
  },
  
  //white knight
  {
    -20,-15,-10,-10,-10,-10,-15,-20,  0,0,0,0,0,0,0,0,
    -15, -5,  0,  2,  2,  0, -5,-15,  0,0,0,0,0,0,0,0,
    -10,  0,  5,  5,  5,  5,  0,-10,  0,0,0,0,0,0,0,0,
    -10,  0,  6, 10, 10,  6,  0,-10,  0,0,0,0,0,0,0,0,
    -10,  0,  6, 12, 12,  6,  0,-10,  0,0,0,0,0,0,0,0,
    -10,  0,  8,  8,  8,  8,  0,-10,  0,0,0,0,0,0,0,0,
    -15, -5,  2,  2,  2,  0, -5,-15,  0,0,0,0,0,0,0,0,
    -20,-15,-10,-10,-10,-10,-15,-20,  0,0,0,0,0,0,0,0
  },
  
  //white bishop
  {
     2, -1, -2, -5, -5, -2, -1,  2, 0,0,0,0,0,0,0,0,
     0,  7,  2,  2,  2,  2,  7,  0, 0,0,0,0,0,0,0,0,
     2,  4,  8,  6,  6,  8,  4,  2, 0,0,0,0,0,0,0,0,
     2,  6,  8, 10, 10,  8,  6,  2, 0,0,0,0,0,0,0,0,
     2,  8,  8, 10, 10,  8,  8,  2, 0,0,0,0,0,0,0,0,
     2,  5,  8,  8,  8,  8,  5,  2, 0,0,0,0,0,0,0,0,
     0,  4,  3,  2,  2,  3,  4,  0, 0,0,0,0,0,0,0,0,
     0,  2,  0,  0,  0,  0,  2,  0, 0,0,0,0,0,0,0,0
  },
  
  
  //white rook
  {
    -1,  1,  3,  4,  4,  3,  1, -1, 0,0,0,0,0,0,0,0,
    -1,  1,  3,  4,  4,  3,  1, -1, 0,0,0,0,0,0,0,0,
    -1,  1,  3,  4,  4,  3,  1, -1, 0,0,0,0,0,0,0,0,
    -1,  1,  3,  4,  4,  3,  1, -1, 0,0,0,0,0,0,0,0,
    -1,  1,  3,  4,  4,  3,  1, -1, 0,0,0,0,0,0,0,0,
     4,  6,  8, 10, 10,  8,  6,  4, 0,0,0,0,0,0,0,0,
     8, 10, 12, 14, 14, 12, 10,  8, 0,0,0,0,0,0,0,0,
     4,  6,  8, 10, 10,  8,  6,  4, 0,0,0,0,0,0,0,0
  },
  
  //white queen
  {
    -5, -4, -3,  0,  0, -3, -4, -5, 0,0,0,0,0,0,0,0,
    -2,  0,  2,  3,  3,  2,  0, -2, 0,0,0,0,0,0,0,0,
     0,  1,  4,  4,  4,  4,  1,  0, 0,0,0,0,0,0,0,0,
     0,  2,  4,  8,  8,  4,  2,  0, 0,0,0,0,0,0,0,0,
     1,  3,  6,  9,  9,  6,  3,  1, 0,0,0,0,0,0,0,0,
     1,  4,  6, 10, 10,  6,  4,  1, 0,0,0,0,0,0,0,0,
     2,  4,  8, 12, 12,  8,  4,  2, 0,0,0,0,0,0,0,0,
    -2,  1,  2,  3,  3,  2,  1, -2, 0,0,0,0,0,0,0,0
    
  },
  
  //white king
  {
      2,  3,  5, -5, -5, -2,  5,  2,  0,0,0,0,0,0,0,0,
     -2, -1,-10,-10,-10,-10, -1, -2,  0,0,0,0,0,0,0,0,
    -10,-10,-10,-10,-10,-10,-10,-10,  0,0,0,0,0,0,0,0,
    -20,-20,-20,-20,-20,-20,-20,-20,  0,0,0,0,0,0,0,0,
    -20,-20,-20,-20,-20,-20,-20,-20,  0,0,0,0,0,0,0,0,
    -20,-20,-20,-20,-20,-20,-20,-20,  0,0,0,0,0,0,0,0,
    -20,-20,-20,-20,-20,-20,-20,-20,  0,0,0,0,0,0,0,0,
    -20,-20,-20,-20,-20,-20,-20,-20,  0,0,0,0,0,0,0,0
  },
  
  //empty
  {0},
  
  //empty
  {0},

  //black pawn
   {	
      0,  0,  0,  0,  0,  0,  0,  0,  0,0,0,0,0,0,0,0,
     65, 80, 85, 90, 90, 85, 80, 65,  0,0,0,0,0,0,0,0,
     12, 20, 20, 25, 25, 20, 20, 12,  0,0,0,0,0,0,0,0,
      4, 12, 12, 14, 14, 12, 12,  4,  0,0,0,0,0,0,0,0,
      0,  4,  4, 16, 16,  4,  4,  0,  0,0,0,0,0,0,0,0,
      0,  0,  0,  4,  4,  0,  0,  0,  0,0,0,0,0,0,0,0,
      0,  0,  0,-12,-12,  0,  0,  0,  0,0,0,0,0,0,0,0,
      0,  0,  0,  0,  0,  0,  0,  0,  0,0,0,0,0,0,0,0
   },
   
  //black knight
  {
    -20,-15,-10,-10,-10,-10,-15,-20,  0,0,0,0,0,0,0,0,
    -15, -5,  2,  2,  2,  0, -5,-15,  0,0,0,0,0,0,0,0,
    -10,  0,  8,  8,  8,  8,  0,-10,  0,0,0,0,0,0,0,0,
    -10,  0,  6, 12, 12,  6,  0,-10,  0,0,0,0,0,0,0,0,
    -10,  0,  6, 10, 10,  6,  0,-10,  0,0,0,0,0,0,0,0,
    -10,  0,  5,  5,  5,  5,  0,-10,  0,0,0,0,0,0,0,0,
    -15, -5,  0,  2,  2,  0, -5,-15,  0,0,0,0,0,0,0,0,
    -20,-15,-10,-10,-10,-10,-15,-20,  0,0,0,0,0,0,0,0
  },
  
  //black bishop
  {
    0,  2,  0,  0,  0,  0,  2,  0,  0,0,0,0,0,0,0,0,
    0,  4,  3,  2,  2,  3,  4,  0,  0,0,0,0,0,0,0,0,
    2,  5,  8,  8,  8,  8,  5,  2,  0,0,0,0,0,0,0,0,
    2,  8,  8, 10, 10,  8,  8,  2,  0,0,0,0,0,0,0,0,
    2,  6,  8, 10, 10,  8,  6,  2,  0,0,0,0,0,0,0,0,
    2,  4,  8,  6,  6,  8,  4,  2,  0,0,0,0,0,0,0,0,
    0,  7,  2,  2,  2,  2,  7,  0,  0,0,0,0,0,0,0,0,
    2, -1, -2, -5, -5, -2, -1,  2,  0,0,0,0,0,0,0,0 
  },
  
  //black rook
  {
     4,  6,  8, 10, 10,  8,  6,  4, 0,0,0,0,0,0,0,0,
     8, 10, 12, 14, 14, 12, 10,  8, 0,0,0,0,0,0,0,0,
     4,  6,  8, 10, 10,  8,  6,  4, 0,0,0,0,0,0,0,0,
    -1,  1,  3,  4,  4,  3,  1, -1, 0,0,0,0,0,0,0,0,
    -1,  1,  3,  4,  4,  3,  1, -1, 0,0,0,0,0,0,0,0,
    -1,  1,  3,  4,  4,  3,  1, -1, 0,0,0,0,0,0,0,0,
    -1,  1,  3,  4,  4,  3,  1, -1, 0,0,0,0,0,0,0,0,
    -1,  1,  3,  4,  4,  3,  1, -1, 0,0,0,0,0,0,0,0 
    
  },
  
  //black queen:
  {
    -2,  1,  2,  3,  3,  2,  1, -2, 0,0,0,0,0,0,0,0,
     2,  4,  8, 12, 12,  8,  4,  2, 0,0,0,0,0,0,0,0,
     1,  4,  6, 10, 10,  6,  4,  1, 0,0,0,0,0,0,0,0,
     1,  3,  6,  9,  9,  6,  3,  1, 0,0,0,0,0,0,0,0,
     0,  2,  4,  8,  8,  4,  2,  0, 0,0,0,0,0,0,0,0,
     0,  1,  4,  4,  4,  4,  1,  0, 0,0,0,0,0,0,0,0,
    -2,  0,  2,  3,  3,  2,  0, -2, 0,0,0,0,0,0,0,0,
    -5, -4, -3,  0,  0, -3, -4, -5, 0,0,0,0,0,0,0,0
    
  },
  
  //black king
  {
    -20,-20,-20,-20,-20,-20,-20,-20,  0,0,0,0,0,0,0,0,
    -20,-20,-20,-20,-20,-20,-20,-20,  0,0,0,0,0,0,0,0,
    -20,-20,-20,-20,-20,-20,-20,-20,  0,0,0,0,0,0,0,0,
    -20,-20,-20,-20,-20,-20,-20,-20,  0,0,0,0,0,0,0,0,
    -20,-20,-20,-20,-20,-20,-20,-20,  0,0,0,0,0,0,0,0,
    -10,-10,-10,-10,-10,-10,-10,-10,  0,0,0,0,0,0,0,0,
     -2, -1,-10,-10,-10,-10, -1, -2,  0,0,0,0,0,0,0,0,
      2,  3,  5, -5, -5, -2,  5,  2,  0,0,0,0,0,0,0,0
  }
};
 
const int endgame_king_psq[2][128] = 
{
  {
    -20,-15,-10,-10,-10,-10,-15,-20,  0,0,0,0,0,0,0,0,
    -15, -5,  0,  0,  0,  0, -5,-11,  0,0,0,0,0,0,0,0,
    -15,  0,  5,  5,  5,  5,  0,-15,  0,0,0,0,0,0,0,0,
     -8,  0,  5, 12, 12,  5,  0, -8,  0,0,0,0,0,0,0,0,
     -8,  0,  5, 12, 12,  5,  0, -8,  0,0,0,0,0,0,0,0,
    -15,  0,  5,  5,  5,  5,  0,-15,  0,0,0,0,0,0,0,0,
    -15, -5,  0,  0,  0,  0, -5,-11,  0,0,0,0,0,0,0,0,
    -20,-15,-10,-10,-10,-10,-15,-20,  0,0,0,0,0,0,0,0
  },

  {
    -20,-15,-10,-10,-10,-10,-15,-20,  0,0,0,0,0,0,0,0,
    -15, -5,  0,  0,  0,  0, -5,-11,  0,0,0,0,0,0,0,0,
    -15,  0,  5,  5,  5,  5,  0,-15,  0,0,0,0,0,0,0,0,
     -8,  0,  5, 12, 12,  5,  0, -8,  0,0,0,0,0,0,0,0,
     -8,  0,  5, 12, 12,  5,  0, -8,  0,0,0,0,0,0,0,0,
    -15,  0,  5,  5,  5,  5,  0,-15,  0,0,0,0,0,0,0,0,
    -15, -5,  0,  0,  0,  0, -5,-11,  0,0,0,0,0,0,0,0,
    -20,-15,-10,-10,-10,-10,-15,-20,  0,0,0,0,0,0,0,0
  }
};
