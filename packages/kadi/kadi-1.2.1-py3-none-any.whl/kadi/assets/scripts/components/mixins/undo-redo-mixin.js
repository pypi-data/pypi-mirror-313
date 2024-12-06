/* Copyright 2020 Karlsruhe Institute of Technology
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License. */

/** Mixin to add basic undo/redo functionality to components. */
export default {
  data() {
    return {
      undoStack: [],
      undoStackIndex: 0,
      undoStackDepth: 10,
    };
  },
  computed: {
    undoable() {
      return this.undoStackIndex > 0;
    },
    redoable() {
      return this.undoStackIndex < (this.undoStack.length - 1);
    },
  },
  methods: {
    /* eslint-disable no-unused-vars */
    getCheckpointData(...args) {
      throw new Error('"getCheckpointData" not implemented.');
    },
    restoreCheckpointData(data) {
      throw new Error('"restoreCheckpointData" not implemented.');
    },
    verifyCheckpointData(currentData, newData) {
      return true;
    },
    /* eslint-enable no-unused-vars */
    saveCheckpoint(...args) {
      const checkpointData = this.getCheckpointData(...args);

      // Give the caller the possibility to not create a new checkpoint after all, e.g. if the data did not actually
      // change but a checkpoint was triggered anyway.
      if (this.undoStack.length > 0
          && !this.verifyCheckpointData(this.undoStack[this.undoStackIndex], checkpointData)) {
        return;
      }

      this.undoStack.splice(this.undoStackIndex + 1);
      this.undoStack.push(checkpointData);
      this.undoStackIndex = this.undoStack.length - 1;

      if (this.undoStack.length > this.undoStackDepth) {
        this.undoStack.shift();
        this.undoStackIndex--;
      }
    },
    resetCheckpoints() {
      this.undoStack = [];
      this.undoStackIndex = 0;
    },
    undo() {
      if (this.undoable) {
        this.undoStackIndex--;
        this.restoreCheckpointData(this.undoStack[this.undoStackIndex]);
      }
    },
    redo() {
      if (this.redoable) {
        this.undoStackIndex++;
        this.restoreCheckpointData(this.undoStack[this.undoStackIndex]);
      }
    },
  },
};
