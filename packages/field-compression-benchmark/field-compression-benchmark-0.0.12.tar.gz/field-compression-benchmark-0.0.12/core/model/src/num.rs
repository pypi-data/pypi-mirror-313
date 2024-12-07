use num_traits::Num;

pub fn half<T: Num>() -> T {
    T::one() / two::<T>()
}

pub fn two<T: Num>() -> T {
    T::one() + T::one()
}
