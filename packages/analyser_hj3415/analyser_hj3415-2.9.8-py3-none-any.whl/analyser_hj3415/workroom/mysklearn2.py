# 필요한 라이브러리 불러오기
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

# 1. 데이터 준비 (주택 면적, 가격)
# 예를 들어 면적에 따른 주택 가격 데이터 (면적: X, 가격: y)
X = np.array([[1500], [2000], [2500], [3000], [3500], [4000]])  # 면적 (단위: square feet)
y = np.array([300000, 400000, 500000, 600000, 700000, 800000])  # 가격 (단위: dollars)

# 2. 학습 데이터와 테스트 데이터를 나누기 (80% 학습, 20% 테스트)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 3. 선형 회귀 모델 생성
model = LinearRegression()

# 4. 모델을 학습시키기 (train 데이터를 사용)
model.fit(X_train, y_train)

# 5. 테스트 데이터로 예측 수행
y_pred = model.predict(X_test)

# 6. 예측 결과 출력
print("실제 값:", y_test)
print("예측 값:", y_pred)

# 7. 시각화를 통해 학습 결과 확인
plt.scatter(X_train, y_train, color='blue', label='Training data')  # 학습 데이터
plt.scatter(X_test, y_test, color='green', label='Test data')  # 실제 값
plt.plot(X_test, y_pred, color='red', label='Prediction')  # 예측된 값
plt.xlabel('House Size (square feet)')
plt.ylabel('Price (dollars)')
plt.legend()
plt.show()

# 9. 모델 평가 (R^2 스코어)
r2_score = model.score(X_test, y_test)
print(f"모델의 R^2 스코어: {r2_score:.2f}")