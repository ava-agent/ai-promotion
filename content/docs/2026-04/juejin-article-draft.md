# 用 React Native 做了一个宠物社交 App，踩了不少坑

说实话，我一直觉得宠物社交这个赛道挺有意思的。上个月看到一个 GitHub 项目叫 **PawPal（宠友圈）**，是用 React Native + Expo + Supabase 做的，功能还挺完整——抖音风格的视频流 + Tinder 式的宠物匹配。Star 数不多，就 1 个，但我看了下代码结构，感觉作者是真的用心了。

我自己之前也试过用 RN 做项目，踩过一堆坑，所以想聊聊这个项目的实现思路，顺便分享一些我在开发过程中遇到的问题。

## 先说说这个项目做对了什么

PawPal 的定位很明确：**让宠物主人们能分享自家毛孩子的日常，还能给宠物"相亲"**。整个技术栈选得也挺合理：

- **React Native + Expo**：快速开发，热更新方便，对独立开发者很友好
- **Supabase**：开源 Firebase 替代品，免费额度够用，PostgreSQL 也能让人安心
- **TypeScript**：类型安全，维护起来不会太痛苦

最让我惊喜的是它的视频流功能。作者用了类似抖音的上下滑动交互，这在 RN 里实现起来其实挺麻烦的。

```typescript
// 视频播放器组件的核心思路
import { Video, ResizeMode } from 'expo-av';
import { Dimensions, FlatList } from 'react-native';

const { height } = Dimensions.get('window');

interface VideoItem {
  id: string;
  uri: string;
  caption: string;
  likes: number;
}

export default function VideoFeed() {
  const [activeIndex, setActiveIndex] = useState(0);
  
  const renderItem = ({ item, index }: { item: VideoItem; index: number }) => (
    <View style={{ height, justifyContent: 'center' }}>
      <Video
        source={{ uri: item.uri }}
        style={{ width: '100%', height: '100%' }}
        resizeMode={ResizeMode.COVER}
        shouldPlay={index === activeIndex}  // 只播放当前可见的视频
        isLooping
        useNativeControls={false}
      />
      {/* 点赞、评论、分享的交互按钮 */}
      <View style={styles.overlay}>
        <Text style={styles.caption}>{item.caption}</Text>
        <LikeButton count={item.likes} />
      </View>
    </View>
  );

  return (
    <FlatList
      data={videos}
      renderItem={renderItem}
      pagingEnabled  // 关键：一页一滑
      vertical
      onViewableItemsChanged={({ viewableItems }) => {
        if (viewableItems.length > 0) {
          setActiveIndex(viewableItems[0].index ?? 0);
        }
      }}
    />
  );
}
```

这里的关键是 `pagingEnabled` 和 `onViewableItemsChanged` 的配合。只让当前屏幕显示的视频播放，其他的暂停，不然性能直接爆炸。这个思路说实话挺实用的。

## Tinder 式宠物匹配是怎么做的

另一个亮点是宠物匹配功能。界面看起来简单，但交互细节很多：

```typescript
import Animated, {
  useAnimatedGestureHandler,
  useSharedValue,
  withSpring,
  interpolate,
  Extrapolate,
} from 'react-native-reanimated';
import { PanGestureHandler } from 'react-native-gesture-handler';

interface PetProfile {
  id: string;
  name: string;
  breed: string;
  age: number;
  photos: string[];
  bio: string;
}

export function PetMatcher({ pets }: { pets: PetProfile[] }) {
  const translateX = useSharedValue(0);
  const translateY = useSharedValue(0);
  
  const gestureHandler = useAnimatedGestureHandler({
    onActive: (event) => {
      translateX.value = event.translationX;
      translateY.value = event.translationY;
    },
    onEnd: (event) => {
      const SWIPE_THRESHOLD = 100;
      
      if (Math.abs(event.translationX) > SWIPE_THRESHOLD) {
        // 滑动距离够大，直接飞出去
        translateX.value = withSpring(
          event.translationX > 0 ? 500 : -500,
          {},
          () => {
            // 动画结束后处理匹配逻辑
            runOnJS(handleSwipe)(event.translationX > 0 ? 'like' : 'pass');
          }
        );
      } else {
        // 不够阈值，弹回来
        translateX.value = withSpring(0);
        translateY.value = withSpring(0);
      }
    },
  });

  const animatedStyle = useAnimatedStyle(() => {
    const rotate = interpolate(
      translateX.value,
      [-200, 0, 200],
      [-30, 0, 30],
      Extrapolate.CLAMP
    );
    
    return {
      transform: [
        { translateX: translateX.value },
        { translateY: translateY.value },
        { rotate: `${rotate}deg` },
      ],
    };
  });

  return (
    <PanGestureHandler onGestureEvent={gestureHandler}>
      <Animated.View style={[styles.card, animatedStyle]}>
        {/* 宠物卡片内容 */}
        <Image source={{ uri: pet.photos[0] }} style={styles.photo} />
        <Text style={styles.name}>{pet.name}, {pet.age}岁</Text>
        <Text style={styles.breed}>{pet.breed}</Text>
      </Animated.View>
    </PanGestureHandler>
  );
}
```

这里用了 `react-native-reanimated` v2 的 worklet 特性，手势和动画都在 UI 线程执行，不会被 JS 线程卡住。我之前试过用普通的 Animated API 做类似效果，一帧一帧地掉，体验很差。换成 reanimated 之后才流畅起来。

## Supabase 后端设计

后端用的是 Supabase，表结构设计我觉得还挺清晰的：

```sql
-- 用户表
CREATE TABLE profiles (
  id UUID REFERENCES auth.users PRIMARY KEY,
  username TEXT UNIQUE NOT NULL,
  avatar_url TEXT,
  created_at TIMESTAMP DEFAULT NOW()
);

-- 宠物表
CREATE TABLE pets (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  owner_id UUID REFERENCES profiles(id) ON DELETE CASCADE,
  name TEXT NOT NULL,
  breed TEXT,
  age INTEGER,
  bio TEXT,
  photos TEXT[],  -- PostgreSQL 数组类型
  created_at TIMESTAMP DEFAULT NOW()
);

-- 匹配表（互相关注）
CREATE TABLE matches (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  pet_a UUID REFERENCES pets(id) ON DELETE CASCADE,
  pet_b UUID REFERENCES pets(id) ON DELETE CASCADE,
  matched_at TIMESTAMP DEFAULT NOW(),
  UNIQUE(pet_a, pet_b)
);

-- 视频内容表
CREATE TABLE posts (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  pet_id UUID REFERENCES pets(id) ON DELETE CASCADE,
  video_url TEXT NOT NULL,
  caption TEXT,
  likes INTEGER DEFAULT 0,
  created_at TIMESTAMP DEFAULT NOW()
);

-- 行级安全策略（RLS）
ALTER TABLE pets ENABLE ROW LEVEL SECURITY;

CREATE POLICY "用户可以查看所有宠物"
  ON pets FOR SELECT
  USING (true);

CREATE POLICY "用户只能修改自己的宠物"
  ON pets FOR UPDATE
  USING (auth.uid() = owner_id);
```

说实话，Supabase 的 RLS（Row Level Security）策略真的是个神器。不用写后端代码就能控制数据权限，对快速原型开发特别友好。我之前用 Firebase 的时候被安全规则折磨得不行，Supabase 的 SQL 方式反而更直观。

## 但说实话，也有一些问题

这个项目不是完美的，我 review 代码时发现了一些值得注意的地方：

**1. 视频加载优化**

现在的实现是滑动到才加载，但如果用户快速滑动，可能会出现白屏。更好的做法是预加载前后各 1-2 个视频，用 `expo-av` 的 `loadAsync` 提前缓冲。

**2. 图片缓存策略**

宠物照片和视频封面图没有用到专门的缓存库，如果用户网络不好，体验会受影响。建议加上 `react-native-fast-image` 或者 Expo 的 `Image` 组件配合 CDN 优化。

**3. 离线支持**

目前是完全依赖网络的，如果地铁里信号不好，App 就基本没法用了。可以考虑用 Redux Persist 或者 WatermelonDB 做本地数据持久化。

**4. 性能瓶颈**

视频流用 FlatList 实现，如果列表很长，内存占用会越来越高。可能需要用到 `react-native-video` 的清理策略，或者考虑用 `FlashList` 替代 FlatList。

## 写在最后

PawPal 这个项目虽然 Star 不多，但作为一个学习资源还挺有价值的。它展示了怎么用现代 RN 技术栈快速搭建一个功能完整的社交 App，代码结构也比较清晰，适合想入坑 React Native 的同学参考。

我自己之前也想过做一个宠物社交产品，但一直没动手。看到有人真的把它做出来，挺受启发的。哈哈，说不定哪天我也 fork 一个版本，加点自己的想法进去。

你们有没有做过类似的社交 App？遇到过什么性能问题吗？或者对宠物社交这个赛道有什么看法？欢迎评论区聊聊 👇

---

**项目地址**：https://github.com/ava-agent/dog-agent
**技术栈**：React Native + Expo + TypeScript + Supabase
**推荐指数**：⭐⭐⭐⭐（适合学习和参考）
