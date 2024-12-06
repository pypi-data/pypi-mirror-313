<!-- Copyright 2024 Karlsruhe Institute of Technology
   -
   - Licensed under the Apache License, Version 2.0 (the "License");
   - you may not use this file except in compliance with the License.
   - You may obtain a copy of the License at
   -
   -     http://www.apache.org/licenses/LICENSE-2.0
   -
   - Unless required by applicable law or agreed to in writing, software
   - distributed under the License is distributed on an "AS IS" BASIS,
   - WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   - See the License for the specific language governing permissions and
   - limitations under the License. -->

<template>
  <div ref="dialog" class="modal" tabindex="-1">
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content">
        <div class="modal-header d-flex align-items-center py-2">
          <span class="modal-title">
            <strong>Score:</strong> {{ score }}
          </span>
          <button type="button" class="close" data-dismiss="modal" @click="gameActive = false">
            <i class="fa-solid fa-xmark fa-xs"></i>
          </button>
        </div>
        <div class="modal-body">
          <div class="menu d-flex flex-column align-items-center">
            <h5 v-if="state === 'start'">Press [Space Bar]</h5>
            <h4 v-if="state === 'over'" class="font-weight-bold">Game Over</h4>
            <h4 v-if="state === 'over'">
              Rank: <strong class="rank" :style="{'color': rank[2]}">{{ rank[1] }}</strong>
            </h4>
          </div>
          <canvas ref="canvas" :width="width" :height="height" class="border border-primary"></canvas>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
canvas {
  vertical-align: bottom;
}

.menu {
  left: 50%;
  position: absolute;
  top: 50%;
  transform: translate(-50%, -50%);
}

.modal-dialog {
  max-width: max-content;
}

.rank {
  text-shadow: -1px 0 black, 0 1px black, 1px 0 black, 0 -1px black;
}
</style>

<script>
export default {
  data() {
    return {
      gameActive: false,
      state: 'start',
      context: null,
      width: 375,
      height: 375,
      grid: 25,
      initialSegments: 5,
      maxScore: 0,
      count: 0,
      score: 0,
      dx: 0,
      dy: 0,
      snake: {
        x: 0,
        y: 0,
        dx: 0,
        dy: 0,
        numSegments: 0,
        segments: [],
      },
      food: {
        x: 0,
        y: 0,
      },
      rank: null,
      ranks: [
        [1, 'S', 'gold'],
        [0.75, 'A', 'lawngreen'],
        [0.3, 'B', 'dodgerblue'],
        [0.1, 'C', 'orchid'],
        [0, 'D', 'tomato'],
      ],
      keyIndex: 0,
      keySequence: [38, 38, 40, 40, 37, 39, 37, 39, 66, 65],
    };
  },
  mounted() {
    this.context = this.$refs.canvas.getContext('2d');
    this.maxScore = ((this.width / this.grid) * (this.width / this.grid)) - this.initialSegments;

    document.addEventListener('keydown', this.keydownHandler);
  },
  beforeDestroy() {
    $(this.$refs.dialog).modal('dispose');
    document.removeEventListener('keydown', this.keydownHandler);
  },
  methods: {
    openGame() {
      this.gameActive = true;
      $(this.$refs.dialog).modal({backdrop: 'static', keyboard: false});
    },
    startGame() {
      this.count = 0;
      this.score = 0;
      this.dx = 1;
      this.dy = 0;

      this.snake.x = Math.floor((this.width / this.grid) / 2) * this.grid;
      this.snake.y = Math.floor((this.height / this.grid) / 2) * this.grid;
      this.snake.numSegments = this.initialSegments;
      this.snake.segments = [];

      this.rank = this.ranks[this.ranks.length - 1];
      this.state = 'play';

      this.generateFood();

      window.requestAnimationFrame(this.gameLoop);
    },
    endGame() {
      for (const rank of this.ranks) {
        const threshold = Math.floor(rank[0] * this.maxScore);

        if (this.score >= threshold) {
          this.rank = rank;
          break;
        }
      }

      this.state = 'over';
      this.context.clearRect(0, 0, this.width, this.width);
    },
    renderGame() {
      this.context.clearRect(0, 0, this.width, this.width);

      // Draw food.
      this.context.fillStyle = 'firebrick';
      this.context.fillRect(this.food.x, this.food.y, this.grid - 1, this.grid - 1);

      // Draw snake.
      this.context.fillStyle = '#00695B';

      for (const segment of this.snake.segments) {
        this.context.fillRect(segment.x, segment.y, this.grid - 1, this.grid - 1);
        this.context.fillStyle = '#009682';
      }
    },
    generateFood() {
      const foodBucket = [];

      for (let x = 0; x < this.width; x += this.grid) {
        for (let y = 0; y < this.width; y += this.grid) {
          if (this.snake.segments.some((segment) => segment.x === x && segment.y === y)) {
            continue;
          }

          foodBucket.push({x, y});
        }
      }

      if (foodBucket.length === 0) {
        this.endGame();
        return;
      }

      const index = Math.floor(Math.random() * foodBucket.length);
      this.food = foodBucket[index];
    },
    gameLoop() {
      if (this.state !== 'play') {
        return;
      }

      window.requestAnimationFrame(this.gameLoop);

      // Game runs at 12 FPS.
      if (++this.count < 5) {
        return;
      }

      this.count = 0;

      // Apply direction and move snake.
      this.snake.dx = this.dx;
      this.snake.dy = this.dy;

      this.snake.x += this.snake.dx * this.grid;
      this.snake.y += this.snake.dy * this.grid;

      // Wrap snake position horizontally.
      if (this.snake.x < 0) {
        this.snake.x = this.width - this.grid;
      } else if (this.snake.x >= this.width) {
        this.snake.x = 0;
      }

      // Wrap snake position vertically.
      if (this.snake.y < 0) {
        this.snake.y = this.width - this.grid;
      } else if (this.snake.y >= this.width) {
        this.snake.y = 0;
      }

      // Keep track of where snake has been.
      this.snake.segments.unshift({x: this.snake.x, y: this.snake.y});

      // Remove segments as we move away from them.
      if (this.snake.segments.length > this.snake.numSegments) {
        this.snake.segments.pop();
      }

      this.renderGame();

      this.snake.segments.forEach((segment, index) => {
        // Check if snake ate the food.
        if (segment.x === this.food.x && segment.y === this.food.y) {
          this.score++;
          this.snake.numSegments++;

          this.generateFood();
          this.renderGame();
        }

        // Check collision with all segments after the current one.
        for (let i = index + 1; i < this.snake.segments.length; i++) {
          if (segment.x === this.snake.segments[i].x && segment.y === this.snake.segments[i].y) {
            this.endGame();
            return;
          }
        }
      });
    },
    keydownHandler(e) {
      if (this.gameActive) {
        e.preventDefault();

        if (this.state === 'play') {
          if (this.snake.dy === 0) {
            if (e.key === 'ArrowUp') {
              this.dy = -1;
              this.dx = 0;
            } else if (e.key === 'ArrowDown') {
              this.dy = 1;
              this.dx = 0;
            }
          }

          if (this.snake.dx === 0) {
            if (e.key === 'ArrowLeft') {
              this.dx = -1;
              this.dy = 0;
            } else if (e.key === 'ArrowRight') {
              this.dx = 1;
              this.dy = 0;
            }
          }
        } else {
          if (e.key === ' ') {
            this.startGame();
          }
        }
      } else {
        this.keyIndex = this.keySequence[this.keyIndex] === e.keyCode ? this.keyIndex + 1 : 0;

        if (this.keyIndex >= this.keySequence.length) {
          this.keyIndex = 0;
          this.openGame();
        }
      }
    },
  },
};
</script>
