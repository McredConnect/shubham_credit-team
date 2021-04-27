function changeState(button, color) {
    document.getElementById(button).style.borderBottom = "3px solid" + color;
    document.getElementById(button).style.color = color;
  }

  function setActive(mode) {
    if (mode == 0) {
      changeState('btn1', '#4CAF50');
      changeState('btn2', '#AAAAAA');
      changeState('btn3', '#AAAAAA');
      changeState('btn4', '#AAAAAA');
    }
    else if (mode == 1) {
      changeState('btn2', '#4CAF50');
      changeState('btn3', '#AAAAAA');
      changeState('btn4', '#AAAAAA');
      changeState('btn1', '#AAAAAA');
    }
    else if (mode == 2) {
      changeState('btn3', '#4CAF50');
      changeState('btn2', '#AAAAAA');
      changeState('btn1', '#AAAAAA');
      changeState('btn4', '#AAAAAA');
    }
    else if (mode == 3) {
      changeState('btn4', '#4CAF50');
      changeState('btn3', '#AAAAAA');
      changeState('btn2', '#AAAAAA');
      changeState('btn1', '#AAAAAA');
    }
  }