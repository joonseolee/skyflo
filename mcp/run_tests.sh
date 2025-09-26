#!/bin/bash

# MCP 테스트 실행 스크립트

echo "🚀 MCP 테스트를 시작합니다..."

# 가상환경 활성화
echo "📦 가상환경을 활성화합니다..."
source test_env/bin/activate

# 테스트 실행
echo "🧪 테스트를 실행합니다..."
python -m pytest tests/ -v

# 커버리지 리포트 생성
echo "📊 커버리지 리포트를 생성합니다..."
python -m pytest tests/ --cov=. --cov-report=html --cov-report=term

echo "✅ 테스트가 완료되었습니다!"
echo "📁 HTML 커버리지 리포트: htmlcov/index.html"
